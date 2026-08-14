#!/usr/bin/env python3
"""
Sageedumint DHT-based sharing & auth
- Uses kademlia DHT (kademlia.network.Server) to store torrent metadata, peers and course index.
- Simple credential system: register/login with bcrypt-hashed passwords, JWT tokens for auth.
- Commands: register, login, whoami, createtorrent, gettorrent, getpeers, seed, download, sharecourse, listcourses, token, exit
Notes: install dependencies:
    pip install PyJWT kademlia transmission-rpc bencodepy bcrypt
"""

import asyncio
import datetime
import json
import jwt
import logging
import os
import time
from pathlib import Path
from transmission_rpc import Client as TransmissionClient
import argparse
import cmd
import sys
import hashlib
import bencodepy
import getpass
import bcrypt

from kademlia.network import Server

# --- Config ---
SECRET_KEY = os.environ.get("SAGE_EDU_SECRET", "your-secure-secret-change-me")
DHT_PORT = int(os.environ.get("SAGE_EDU_DHT_PORT", 8468))
BOOTSTRAP_NODE = (os.environ.get("SAGE_EDU_BOOT_IP", "127.0.0.1"), int(os.environ.get("SAGE_EDU_BOOT_PORT", DHT_PORT)))
LOG_FILE = "sageedumint.log"
TORRENT_DIR = "torrents"
USERS_FILE = "users.json"   # stores {username: {pw_hash:..., role:..., created:...}}
COURSE_INDEX_KEY = "courses_index"  # DHT key where array of course entries is stored

# --- Logging Setup ---
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

os.makedirs(TORRENT_DIR, exist_ok=True)

# --- Helper: user storage ---
def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

# --- JWT Auth ---
def generate_token(payload: dict, expiry_minutes=60) -> str:
    payload = dict(payload)  # copy
    payload["exp"] = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=expiry_minutes)
    payload["iat"] = datetime.datetime.now(datetime.timezone.utc)
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expired")
    except jwt.InvalidTokenError as e:
        raise ValueError(f"Invalid token: {e}")

# --- Torrent Creation (no required trackers by default) ---
def create_torrent(file_path: str, trackers: list = None, comment: str = "Sageedumint educational content") -> str:
    """Create a torrent file for the given file path. Keeps trackers optional (DHT-first)."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} does not exist")
    
    if trackers is None:
        trackers = []  # DHT usage removes need for trackers, but keep optional

    info = {
        b'name': os.path.basename(file_path).encode('utf-8'),
        b'piece length': 256 * 1024,
        b'pieces': b'',
        b'length': os.path.getsize(file_path),
        b'private': 0
    }

    piece_length = info[b'piece length']
    pieces = b''
    with open(file_path, 'rb') as f:
        while True:
            piece = f.read(piece_length)
            if not piece:
                break
            pieces += hashlib.sha1(piece).digest()
    info[b'pieces'] = pieces

    # Build torrent dict with byte-keys for bencode
    torrent = {
        b'info': info,
        b'creation date': int(time.time()),
        b'created by': b'Sageedumint',
        b'comment': comment.encode('utf-8'),
        b'encoding': b'UTF-8'
    }
    if trackers:
        torrent[b'announce'] = trackers[0].encode('utf-8')
        torrent[b'announce-list'] = [[t.encode('utf-8') for t in trackers]]

    #bencoder = bencodepy.encode(encoding='utf-8', dict_ordered=True)
    torrent_data = bencodepy.encode(torrent)
    torrent_name = f"{os.path.basename(file_path)}.torrent"
    torrent_path = os.path.join(TORRENT_DIR, torrent_name)
    with open(torrent_path, 'wb') as f:
        f.write(torrent_data)

    logging.info(f"Created torrent: {torrent_path}")
    return torrent_path

def get_torrent_info_hash(torrent_path: str) -> str:
    with open(torrent_path, 'rb') as f:
        torrent_data = f.read()
    #bencoder = bencodepy.decode(encoding='utf-8', dict_ordered=True)
    torrent_dict = bencodepy.decode(torrent_data)
    info = torrent_dict[b'info']
    info_encoded = bencodepy.encode(info)
    return hashlib.sha1(info_encoded).hexdigest()

# --- DHT Node ---
class DHTNode:
    def __init__(self, port=DHT_PORT):
        self.server = Server()
        self.port = port
        # create dedicated loop (useful for blocking CLI use)
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def start(self, bootstrap_ip=None, bootstrap_port=None):
        async def _start():
            await self.server.listen(self.port)
            if bootstrap_ip and bootstrap_port:
                try:
                    await self.server.bootstrap([(bootstrap_ip, bootstrap_port)])
                except Exception as e:
                    logging.warning(f"Bootstrap failed: {e}")
            logging.info(f"DHT node started on port {self.port}")
        self.loop.run_until_complete(_start())

    def store(self, key: str, value: str):
        async def _store():
            await self.server.set(key, value)
            logging.info(f"Stored DHT key: {key}")
        self.loop.run_until_complete(_store())

    def retrieve(self, key: str):
        async def _get():
            v = await self.server.get(key)
            logging.info(f"Retrieved DHT key: {key}")
            return v
        return self.loop.run_until_complete(_get())

    # convenience for torrents
    def store_torrent(self, info_hash: str, torrent_data):
        self.store(f"torrent_{info_hash}", torrent_data)

    def retrieve_torrent(self, info_hash: str):
        return self.retrieve(f"torrent_{info_hash}")

    def store_peer(self, info_hash: str, peer_address: str):
        async def _store():
            key = f"peers_{info_hash}"
            existing = await self.server.get(key) or "[]"
            peers = json.loads(existing)
            if peer_address not in peers:
                peers.append(peer_address)
                await self.server.set(key, json.dumps(peers))
                logging.info(f"Stored peer in DHT: {peer_address} -> {info_hash}")
        self.loop.run_until_complete(_store())

    def retrieve_peers(self, info_hash: str):
        val = self.retrieve(f"peers_{info_hash}")
        if val:
            return json.loads(val)
        return []

    # Course index helpers: maintain a list at COURSES_INDEX_KEY
    def add_course(self, course_meta: dict):
        async def _add():
            existing = await self.server.get(COURSE_INDEX_KEY) or "[]"
            courses = json.loads(existing)
            courses.append(course_meta)
            await self.server.set(COURSE_INDEX_KEY, json.dumps(courses))
            logging.info(f"Added course to index: {course_meta.get('title')}")
        self.loop.run_until_complete(_add())

    def list_courses(self):
        val = self.retrieve(COURSE_INDEX_KEY)
        if val:
            return json.loads(val)
        return []

    def close(self):
        try:
            self.loop.run_until_complete(self.server.stop())
        except Exception:
            pass
        self.loop.close()

# --- Torrent Peer (seeding & downloading via Transmission) ---
def seed_file(torrent_path: str, dht_node: DHTNode = None, peer_id_hint: str = None):
    try:
        client = TransmissionClient()  # connects to local transmission
        torrent = client.add_torrent(torrent=torrent_path)
        logging.info(f"Added torrent to Transmission for seeding: {torrent_path}")

        info_hash = get_torrent_info_hash(torrent_path)
        # store torrent metadata and a synthetic peer id to DHT
        if dht_node:
            file_path = torrent_path.replace('.torrent', '')
            torrent_data = {
                "name": os.path.basename(torrent_path),
                "created": int(time.time()),
                "size": os.path.getsize(file_path) if os.path.exists(file_path) else 0
            }
            dht_node.store_torrent(info_hash, json.dumps(torrent_data))
            peer_id = peer_id_hint or f"peer_{hashlib.md5(str(time.time()).encode()).hexdigest()[:8]}"
            dht_node.store_peer(info_hash, peer_id)

        # wait until seeding (non-blocking minimal sleep)
        while not torrent.is_seed:
            time.sleep(1)
            torrent = client.get_torrent(torrent.id)
        logging.info("Seeding complete.")
        return True, info_hash
    except Exception as e:
        logging.error(f"Error seeding file: {e}")
        return False, None

def download_file(magnet_uri: str, dht_node: DHTNode = None):
    try:
        client = TransmissionClient()
        torrent = client.add_torrent(magnet=magnet_uri)
        logging.info("Added magnet to Transmission for download")
        # extract info hash
        if "xt=urn:btih:" in magnet_uri:
            info_hash = magnet_uri.split("xt=urn:btih:")[1].split("&")[0]
            if dht_node:
                peers = dht_node.retrieve_peers(info_hash)
                if peers:
                    logging.info(f"Found {len(peers)} peers in DHT for {info_hash}")
        while not torrent.is_finished:
            time.sleep(1)
            torrent = client.get_torrent(torrent.id)
        logging.info("Download complete.")
        return True
    except Exception as e:
        logging.error(f"Error downloading file: {e}")
        return False

# --- Authentication helpers (bcrypt) ---
def register_user(username: str, password: str, role: str = "student"):
    users = load_users()
    if username in users:
        raise ValueError("Username already exists")
    salt = bcrypt.gensalt()
    pw_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")
    users[username] = {"pw_hash": pw_hash, "role": role, "created": int(time.time())}
    save_users(users)
    logging.info(f"Registered user: {username}")

def authenticate_user(username: str, password: str) -> bool:
    users = load_users()
    user = users.get(username)
    if not user:
        return False
    return bcrypt.checkpw(password.encode("utf-8"), user["pw_hash"].encode("utf-8"))

def get_user_role(username: str):
    users = load_users()
    u = users.get(username)
    return u.get("role") if u else None

# --- CLI ---
class SageedumintCLI(cmd.Cmd):
    intro = "Welcome to Sageedumint DHT Tracker. Type 'help' or '?' to list commands.\n"
    prompt = "sageedumint> "

    def __init__(self, node: DHTNode):
        super().__init__()
        self.node = node
        self.current_token = None
        self.current_user = None

    # ----- Auth commands -----
    def do_register(self, arg):
        """register <username> -- interactively prompts for password"""
        args = arg.split()
        if not args:
            print("Usage: register <username>")
            return
        username = args[0]
        password = getpass.getpass("Password: ")
        password2 = getpass.getpass("Confirm Password: ")
        if password != password2:
            print("Passwords do not match")
            return
        try:
            register_user(username, password)
            print(f"Registered user {username}")
        except Exception as e:
            print(f"Error: {e}")

    def do_login(self, arg):
        """login <username> -- prompts for password and delivers JWT token"""
        args = arg.split()
        if not args:
            print("Usage: login <username>")
            return
        username = args[0]
        password = getpass.getpass("Password: ")
        if authenticate_user(username, password):
            role = get_user_role(username)
            token = generate_token({"user": username, "role": role}, expiry_minutes=120)
            self.current_token = token
            self.current_user = {"user": username, "role": role}
            print("Login successful. Token stored in session.")
            print(f"Token (short): {token[:40]}...")  # do not print full token always
        else:
            print("Invalid credentials")

    def do_whoami(self, arg):
        """whoami -- show current authenticated user"""
        if not self.current_token:
            print("Not logged in")
            return
        try:
            payload = verify_token(self.current_token)
            print(f"Logged in as: {payload.get('user')} (role: {payload.get('role')})")
        except ValueError as e:
            print(f"Token invalid: {e}")
            self.current_token = None
            self.current_user = None

    # ----- Helpers -----
    def require_auth(self):
        if not self.current_token:
            raise PermissionError("Authentication required. Use 'login' first.")
        try:
            payload = verify_token(self.current_token)
            return payload
        except ValueError as e:
            self.current_token = None
            self.current_user = None
            raise PermissionError(f"Token invalid: {e}")

    # ----- Torrent & DHT commands -----
    def do_createtorrent(self, arg):
        """Create a torrent file and store metadata in DHT: createtorrent <file_path> [trackers...]"""
        try:
            self.require_auth()
        except PermissionError as e:
            print(e)
            return

        args = arg.split()
        if not args:
            print("Error: file path is required")
            return
        file_path = args[0]
        trackers = args[1:] if len(args) > 1 else None
        try:
            torrent_path = create_torrent(file_path, trackers)
            info_hash = get_torrent_info_hash(torrent_path)
            magnet_uri = f"magnet:?xt=urn:btih:{info_hash}&dn={os.path.basename(file_path)}"

            torrent_data = {
                "name": os.path.basename(file_path),
                "created": int(time.time()),
                "size": os.path.getsize(file_path),
                "magnet_uri": magnet_uri,
                "torrent_path": torrent_path,
                "shared_by": self.current_user.get("user")
            }
            self.node.store_torrent(info_hash, json.dumps(torrent_data))
            print(f"Created torrent: {torrent_path}")
            print(f"Info Hash: {info_hash}")
            print(f"Magnet URI: {magnet_uri}")
            print("Torrent info stored in DHT")
        except Exception as e:
            print(f"Error creating torrent: {e}")

    def do_gettorrent(self, arg):
        """Get torrent metadata from DHT: gettorrent <info_hash>"""
        try:
            self.require_auth()
        except PermissionError as e:
            print(e)
            return
        if not arg:
            print("Error: info hash is required")
            return
        try:
            torrent_data = self.node.retrieve_torrent(arg)
            if torrent_data:
                data = json.loads(torrent_data)
                created = datetime.datetime.fromtimestamp(data.get("created", 0))
                print(f"Torrent Name: {data.get('name', 'Unknown')}")
                print(f"Size: {data.get('size', 0)} bytes")
                print(f"Created: {created}")
                print(f"Magnet URI: {data.get('magnet_uri', 'Not available')}")
                print(f"Shared by: {data.get('shared_by', 'unknown')}")
            else:
                print("Torrent not found in DHT")
        except Exception as e:
            print(f"Error retrieving torrent: {e}")

    def do_getpeers(self, arg):
        """Get peers for a torrent: getpeers <info_hash>"""
        try:
            self.require_auth()
        except PermissionError as e:
            print(e)
            return
        if not arg:
            print("Error: info hash is required")
            return
        try:
            peers = self.node.retrieve_peers(arg)
            if peers:
                print(f"Found {len(peers)} peers for torrent {arg}:")
                for p in peers:
                    print(f"  - {p}")
            else:
                print("No peers found for this torrent")
        except Exception as e:
            print(f"Error retrieving peers: {e}")

    def do_seed(self, arg):
        """Seed a file using local Transmission: seed <file_path>"""
        try:
            self.require_auth()
        except PermissionError as e:
            print(e)
            return
        if not arg:
            print("Error: file path is required")
            return
        success, info_hash = seed_file(arg, self.node, peer_id_hint=self.current_user.get("user"))
        if success:
            print(f"Seeding file: {arg}")
            print(f"Info Hash: {info_hash}")
        else:
            print(f"Failed to seed file: {arg}")

    def do_download(self, arg):
        """Download a file via magnet URI: download <magnet_uri>"""
        try:
            self.require_auth()
        except PermissionError as e:
            print(e)
            return
        if not arg:
            print("Error: magnet URI is required")
            return
        if download_file(arg, self.node):
            print(f"Downloading from: {arg}")
        else:
            print(f"Failed to download from: {arg}")

    # ----- Course sharing -----
    def do_sharecourse(self, arg):
        """sharecourse <file_path> <course_title> -- creates torrent + stores course metadata in DHT"""
        try:
            self.require_auth()
        except PermissionError as e:
            print(e)
            return
        parts = arg.split(maxsplit=1)
        if len(parts) < 2:
            print("Usage: sharecourse <file_path> <course_title>")
            return
        file_path, title = parts[0], parts[1].strip()
        try:
            torrent_path = create_torrent(file_path)
            info_hash = get_torrent_info_hash(torrent_path)
            magnet_uri = f"magnet:?xt=urn:btih:{info_hash}&dn={os.path.basename(file_path)}"
            # store torrent metadata
            torrent_data = {
                "name": os.path.basename(file_path),
                "created": int(time.time()),
                "size": os.path.getsize(file_path),
                "magnet_uri": magnet_uri,
                "torrent_path": torrent_path,
                "shared_by": self.current_user.get("user")
            }
            self.node.store_torrent(info_hash, json.dumps(torrent_data))
            # add to course index
            course_meta = {
                "title": title,
                "info_hash": info_hash,
                "magnet_uri": magnet_uri,
                "shared_by": self.current_user.get("user"),
                "created": int(time.time())
            }
            self.node.add_course(course_meta)
            print(f"Course '{title}' shared. Info Hash: {info_hash}")
        except Exception as e:
            print(f"Error sharing course: {e}")

    def do_listcourses(self, arg):
        """List courses stored in DHT index: listcourses"""
        try:
            self.require_auth()
        except PermissionError as e:
            print(e)
            return
        try:
            courses = self.node.list_courses()
            if not courses:
                print("No courses found.")
                return
            for i, c in enumerate(courses, 1):
                created = datetime.datetime.fromtimestamp(c.get("created", 0))
                print(f"{i}. {c.get('title')} (shared_by: {c.get('shared_by')}, created: {created})")
                print(f"    magnet: {c.get('magnet_uri')}")
                print(f"    info_hash: {c.get('info_hash')}")
        except Exception as e:
            print(f"Error listing courses: {e}")

    def do_token(self, arg):
        """token <user_id> -- generate a JWT token (admin use)"""
        try:
            payload = self.require_auth()
            # only allow admins to generate arbitrary tokens if desired
            if payload.get("role") != "admin":
                print("Only admin can generate arbitrary tokens")
                return
        except PermissionError as e:
            print(e)
            return

        if not arg:
            print("Usage: token <user_id>")
            return
        token = generate_token({"user": arg, "role": "student"}, expiry_minutes=60)
        print(f"JWT Token: {token}")

    def do_exit(self, arg):
        """Exit the application"""
        print("Goodbye!")
        try:
            self.node.close()
        except Exception:
            pass
        return True

# --- CLI arg parsing & main ---
def parse_args():
    parser = argparse.ArgumentParser(description="Sageedumint - DHT Tracker with auth & course sharing")
    parser.add_argument("-i", "--interactive", action="store_true", help="Start interactive CLI")
    parser.add_argument("--createtorrent", metavar="FILE_PATH", help="Create a torrent file")
    parser.add_argument("--gettorrent", metavar="INFO_HASH", help="Get torrent from DHT")
    parser.add_argument("--getpeers", metavar="INFO_HASH", help="Get peers for a torrent")
    parser.add_argument("--seed", metavar="FILE_PATH", help="Seed a file")
    parser.add_argument("--download", metavar="MAGNET_URI", help="Download a file from magnet URI")
    parser.add_argument("--token", metavar="USER_ID", help="Generate a JWT token for a user (admin only)")
    parser.add_argument("--register", metavar="USERNAME", help="Register a user")
    parser.add_argument("--login", metavar="USERNAME", help="Login (prints token)")
    return parser.parse_args()

def main():
    args = parse_args()

    node = DHTNode()
    node.start(*BOOTSTRAP_NODE)

    # CLI interactive or single command
    if args.register:
        username = args.register
        pw = getpass.getpass("Password: ")
        try:
            register_user(username, pw)
            print(f"Registered {username}")
        except Exception as e:
            print(f"Error registering: {e}")
        node.close()
        return

    if args.login:
        username = args.login
        pw = getpass.getpass("Password: ")
        if authenticate_user(username, pw):
            role = get_user_role(username)
            token = generate_token({"user": username, "role": role}, expiry_minutes=120)
            print(f"Token: {token}")
        else:
            print("Invalid credentials")
        node.close()
        return

    # Non-interactive torrent commands:
    if args.createtorrent:
        # this CLI path does not authenticate; recommend using interactive CLI for auth
        try:
            torrent_path = create_torrent(args.createtorrent)
            info_hash = get_torrent_info_hash(torrent_path)
            magnet_uri = f"magnet:?xt=urn:btih:{info_hash}&dn={os.path.basename(args.createtorrent)}"
            torrent_data = {
                "name": os.path.basename(args.createtorrent),
                "created": int(time.time()),
                "size": os.path.getsize(args.createtorrent),
                "magnet_uri": magnet_uri,
                "torrent_path": torrent_path
            }
            node.store_torrent(info_hash, json.dumps(torrent_data))
            print(f"Created torrent: {torrent_path}")
            print(f"Info Hash: {info_hash}")
            print(f"Magnet URI: {magnet_uri}")
        except Exception as e:
            print(f"Error creating torrent: {e}")

    if args.gettorrent:
        torrent_data = node.retrieve_torrent(args.gettorrent)
        if torrent_data:
            data = json.loads(torrent_data)
            print(f"Torrent Name: {data.get('name', 'Unknown')}")
            print(f"Size: {data.get('size', 0)} bytes")
            print(f"Created: {datetime.datetime.fromtimestamp(data.get('created', 0))}")
            print(f"Magnet URI: {data.get('magnet_uri', 'Not available')}")
        else:
            print("Torrent not found in DHT")

    if args.getpeers:
        peers = node.retrieve_peers(args.getpeers)
        if peers:
            print(f"Found {len(peers)} peers:")
            for p in peers:
                print(f"  - {p}")
        else:
            print("No peers found")

    if args.seed:
        success, info_hash = seed_file(args.seed, node)
        if success:
            print(f"Seeding file: {args.seed}")
            print(f"Info Hash: {info_hash}")
        else:
            print(f"Failed to seed file: {args.seed}")

    if args.download:
        if download_file(args.download, node):
            print(f"Downloading from: {args.download}")
        else:
            print(f"Failed to download from: {args.download}")

    if args.token:
        token = generate_token({"user": args.token}, expiry_minutes=60)
        print(f"JWT Token: {token}")

    # Start interactive mode if requested or no other commands
    if args.interactive or not any([args.createtorrent, args.gettorrent, args.getpeers, args.seed, args.download, args.token, args.register, args.login]):
        cli = SageedumintCLI(node)
        cli.cmdloop()
    else:
        node.close()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        print(f"Error: {e}")
