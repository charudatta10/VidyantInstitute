import Head from 'next/head'

export default function AcademicStructure() {
  return (
    <div>
      <Head>
        <title>Academic Structure - OpenDAO University</title>
        <meta name="description" content="The academic structure of OpenDAO University" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main>
        <h1>
          Academic Structure
        </h1>

        <table>
          <thead>
            <tr>
              <th>Stage</th>
              <th>Duration</th>
              <th>Credential</th>
              <th>Focus</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>🧠 Foundation</td>
              <td>4 years</td>
              <td>Foundational Certificate NFT</td>
              <td>PKM, interdisciplinary exposure, cognitive scaffolding</td>
            </tr>
            <tr>
              <td>🎓 Diploma</td>
              <td>1 year</td>
              <td>Diploma NFT</td>
              <td>Applied skills, domain-specific orientation</td>
            </tr>
            <tr>
              <td>🎓 Degree</td>
              <td>2 years</td>
              <td>Bachelor's NFT</td>
              <td>Research basics, modular inquiry, community projects</td>
            </tr>
            <tr>
              <td>🎓 Masters</td>
              <td>1 year</td>
              <td>Master's NFT</td>
              <td>Advanced synthesis, AI-assisted research</td>
            </tr>
            <tr>
              <td>🎓 PhD</td>
              <td>2 years</td>
              <td>Doctoral NFT</td>
              <td>Original contribution, DAO governance, open publication</td>
            </tr>
          </tbody>
        </table>
      </main>
    </div>
  )
}
