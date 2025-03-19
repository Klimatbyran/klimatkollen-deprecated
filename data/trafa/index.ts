/* eslint-disable no-continue */
/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable @typescript-eslint/no-explicit-any */
/* eslint-disable no-plusplus */
/* eslint-disable no-console */
import axios, { AxiosError } from 'axios'
import fs from 'fs'
import readline from 'readline'
import { exec, spawn } from 'child_process'
import { Row, TrafaResponseObject } from './types'
import { TrafaClient } from './client'

type ResultInterface = {
  ar : string
  drivmedel: string
  reglan: string
  regkom: string
  nyregunder: number
  itrfslut: number

}
type DesiredInterface = {
  year : string
  name : string
  totalElectricCars : number
  totalCarsInTraffic : number
  totalCars : number
  percentageElectricCars : number
}

export const TRAFA_BASE_URL = 'https://api.trafa.se/api/data'
const TIMESTAMP = new Date().toISOString()
/**
 * Axios instance for making requests to the TRAFA API.
 */
const trafaApi = axios.create({
  baseURL: TRAFA_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add a response interceptor to the axios instance
trafaApi.interceptors.response.use((response) => {
  const res = response.data
  // if the response contains errors, throw an error with the error messages joined by a comma
  if (res?.Errors?.length > 0) {
    throw new Error(res.Errors.map((e: string) => e).join(', '))
  }
  return response
})

/**
 * Fetches Trafa data based on the provided query.
 * @param query - The query string to search for Trafa data.
 * @returns A Promise that resolves to a TrafaResponseObject.
 * @throws An Error if the data fetching fails.
 */
export const fetchTrafaData = async (query: string): Promise<TrafaResponseObject> => {
  try {
    const res = await trafaApi.get(`?query=${query}`)
    return res.data
  } catch (error : any) {
    if (axios.isAxiosError(error)) {
      const axiosError = error as AxiosError
      // @ts-expect-error response is not always defined
      console.error(axiosError.response?.data?.Message ?? axiosError.message)
    } else {
      throw new Error(error?.message ?? 'Failed to fetch data from Trafa')
    }
    throw new Error('Failed to fetch data from Trafa')
  }
}

/**
 * Retrieves the current Git user name.
 * @returns A promise that resolves with the current Git user name.
 */
const currentGitUser = () => new Promise<string>((resolve, reject) => {
  exec('git config user.name', (error, stdout) => {
    if (error) {
      reject(error)
    } else {
      resolve(stdout.trim())
    }
  })
})

/**
 * Writes the provided data to a file and saves metadata containing the last fetched date and git user name.
 * @param data - The data to be written to the file.
 */
const saveJson = async <T>({
  data,
  outputFolder = 'data/trafa/downloads',
  fileName = 'trafa-data.json',
}: {
  data: T
  outputFolder?: string
  fileName?: string
}) => {
  const filePath = `${outputFolder}/${fileName}`
  const metadataPath = `${outputFolder}/metadata.yml`
  if (!fs.existsSync(outputFolder)) {
    fs.mkdirSync(outputFolder, { recursive: true })
  }
  const currentUser = (await currentGitUser()) ?? 'unknown'
  const metadata = `lastFetched: ${new Date().toLocaleString('sv')}\nlastFetchedBy: ${currentUser}`
  fs.writeFileSync(filePath, JSON.stringify(data, null, 2))
  fs.writeFileSync(metadataPath, metadata)
}

/**
 * Processes Trafadata rows and returns a new array with processed data tranforming the data into a more usable format.
 * e.g converting string to number whre required.
 * @param rows - Trafadata rows array to be processed.
 */
const processRows = (rows: Row[]) => rows.map((row) => {
  const result: ResultInterface = {} as ResultInterface
  row.Cell.forEach((cell) => {
    const isNumber = !Number.isNaN(parseInt(cell.Value, 10));
    // eslint-disable-next-line @typescript-eslint/no-explicit-any -- any type is used to dynamically assign properties to the result object
    (result as any)[cell.Column] = isNumber ? parseInt(cell.Value, 10) : cell.Value
  })
  return result
})
/**
 * Tranforms the processed data and performs calculations.
 * @param data - The processed data to be aggregated.
 * @returns
 */
const aggregateData = (data: ResultInterface[]) => {
  const aggregationMap = new Map<string, DesiredInterface>()
  const keyMatchCount = new Map<string, number>()

  try {
    for (let i = 0; i < data.length; i++) {
      const entry = data[i]

      if (!entry.regkom || !entry.ar || entry.nyregunder === undefined || entry.itrfslut === undefined) {
        console.error(`Invalid entry encountered: ${JSON.stringify(entry)}`)
        continue
      }
      if (entry.regkom === 'Totalt') { continue }

      const key = `${entry.regkom}-${entry.ar}`

      // Skip "Okänd kommun" entries
      if (key.includes('Okänd')) {
        continue
      }

      // check if the row is a total row (contains total number of newly registered cars for all fuel types)
      const isTotalRow = entry.drivmedel === 'Totalt'

      // create a new entry in the aggregation map if it doesn't exist yet
      if (!aggregationMap.has(key)) {
        aggregationMap.set(key, {
          year: entry.ar,
          name: entry.regkom,
          totalCarsInTraffic: 0,
          totalElectricCars: 0,
          totalCars: 0,
          percentageElectricCars: 0,
        })
      }

      const aggregatedEntry = aggregationMap.get(key)!

      // count how many times a key is matched
      const count = keyMatchCount.get(key) || 0

      if (isTotalRow) {
        aggregatedEntry.totalCars += entry.nyregunder
      } else {
        aggregatedEntry.totalElectricCars += entry.nyregunder
        aggregatedEntry.totalCarsInTraffic += entry.itrfslut
      }

      // increment the count of how many times a key is matched
      keyMatchCount.set(key, count + 1)

      if (count + 1 === 3) {
        // make sure totalCars is not NaN
        if (!Number.isNaN(aggregatedEntry.totalCars)) {
          // assumming there are 3 rows per municipality per year (total, electric cars, and hybrid cars) calculate the percentage of electric cars
          const percentageChange = (aggregatedEntry.totalElectricCars / aggregatedEntry.totalCars).toPrecision()
          aggregatedEntry.percentageElectricCars = parseFloat(percentageChange)
        }
      }
      // remove the total row from the aggregation map
      if (aggregatedEntry.name === 'Totalt') {
        aggregationMap.delete(key)
      }
    }
    return Array.from(aggregationMap.values()).sort((a, b) => a.name.localeCompare(b.name))
  } catch (error) {
    console.error(`Aggregation failed: ${error}`)
    throw new Error('Aggregation failed')
  }
}

// Helper function to get the year from rows
const getYear = (rows: any[]): string => rows[0]?.Cell.find((cell: any) => cell.Column === 'ar')?.Value ?? 'unknown'

/**
 * Checks if the Git worktree is empty.
 * @returns A promise that resolves to a boolean indicating whether the worktree is empty or not.
 */
const isEmptyWorktree = () => {
  exec('git status --porcelain', (error, stdout) => {
    if (error) {
      console.error('%s: (ERROR) Failed to check if the worktree is empty.', TIMESTAMP)
      console.error('%s: Exiting...', TIMESTAMP)
      setTimeout(() => process.exit(1), 1000)
    } else if (stdout.trim() !== '') {
      console.error('%s: (ERROR) Uncommitted changes in the repository. Please commit or stash them before running this script.', TIMESTAMP)
      console.error('%s: Exiting...', TIMESTAMP)
      setTimeout(() => process.exit(1), 1000)
    }
  })
  return true
}

/**
 * Asks the user if they want to commit the changes to the repository.
 * If the user answers 'y', it adds, commits, and pushes the changes to the repository.
 * Closes the readline interface after execution.
 */
function askForCommit() {
  const rl = readline.createInterface({ input: process.stdin, output: process.stdout })
  rl.question(
    'Do you want to commit the changes to the repository? (y/n) ',
    async (answer) => {
      if (answer === 'y') {
        exec(
          'git add . && git commit -m "chore: Update Trafa electric car data" && git push',
          (error, stdout) => {
            if (error) {
              console.error(error)
            } else {
              console.log(`%s: ${stdout}`, TIMESTAMP)
              console.log('%s: Changes committed successfully!', TIMESTAMP)
            }
          },
        )
      }
      console.log('%s: Script execution complete! Exiting...', TIMESTAMP)
      rl.close()
    },
  )
}

const getMetadata = () => {
  const metadataPath = 'data/trafa/downloads/metadata.yml'
  if (!fs.existsSync(metadataPath)) {
    return {
      lastFetched: new Date(0),
      lastFetchedBy: 'unknown',
    }
  }
  const metadata = fs.readFileSync(metadataPath, 'utf8')
  const [lastFetched, lastFetchedBy] = metadata.split('\n').map((line) => line.split(': ')[1])
  return {
    lastFetched: new Date(lastFetched),
    lastFetchedBy,
  }
}
const seperator = '---------------------------------------------------------------------------------'
const main = async () => {
  [
    'This script fetches data from the TRAFA API and processes the response and saves it to a file.',
    seperator,
    'The data is fetched for the years 2015 to the previous year, skipping the current year.',
    'for the following fuel types: el, laddhybrid, and totalt(total number of registered cars).',
    'nyregunder(number of newly registered cars), and itrfslut(number of cars in traffic).',
    'also commits the changes(trafa-data.json & metadata-yml)  to the repository after processing the data.',
    seperator,
  ].forEach((message, i) => console.log(`%s: ${message}`, TIMESTAMP))

  const metadata = getMetadata()
  const today = new Date()

  // Check if the data should be revalidated if the data is older than a year or the environment variable is set to true
  const shouldFetch = process.env.NEXT_PUBLIC_REVALIDATE_TRAFA_DATA === 'true' ? true : today.getFullYear() - metadata.lastFetched.getFullYear() > 1
  console.log('%s: "ENV_REVALIDATE_TRAFA_DATA": %s', TIMESTAMP, process.env.NEXT_PUBLIC_REVALIDATE_TRAFA_DATA)
  if (metadata.lastFetchedBy !== 'unknown') {
    console.log(
      '%s: Last fetched on %s by %s',
      TIMESTAMP,
      metadata.lastFetched.toLocaleString('sv'),
      metadata.lastFetchedBy,
    )
  } else {
    console.log('%s: No previous fetch metadata found.', TIMESTAMP)
  }
  if (!shouldFetch) {
    console.log('%s: Data is up to date. Exiting...', TIMESTAMP)
    process.exit(0)
  }

  isEmptyWorktree()

  const client = new TrafaClient()
  const currentYear = new Date().getFullYear()
  const yearsFrom2015 = Array.from({ length: currentYear - 2015 + 1 }, (_, i) => 2015 + i)
  // remove current year from list this data is not available yet
  yearsFrom2015.pop()

  try {
    const queries = yearsFrom2015?.map((year) => client
      .setYear(year.toString())
      .setMeasure(['nyregunder', 'itrfslut'])
      .setTarget({ category: 'communal', target: 'cars' })
      .setFuel(['el', 'laddhybrid', 'totalt'])
      .build())

    const result = await Promise.allSettled(
      queries.map((query) => fetchTrafaData(query.query)),
    )

    const processedData: {
        municipalities: DesiredInterface[]
        year: string
      }[] = []

    result?.forEach((d) => {
      if (d.status === 'fulfilled') {
        const cellData = processRows(d.value.Rows)
        const aggregatedData = aggregateData(cellData) ?? []
        const year = getYear(d.value.Rows)
        processedData?.push({ year, municipalities: aggregatedData })
      }
    })
    await saveJson({ data: processedData, fileName: 'trafa-data.json' })
    askForCommit()
  } catch (error) {
    console.error(`%s: ${error}`, TIMESTAMP)
  }
}

main()
