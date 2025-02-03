/* eslint-disable @typescript-eslint/no-explicit-any */
import * as fs from 'fs'
import * as path from 'path'
import {
  Municipality,
  EmissionPerYear,
  EmissionSector,
  Budget,
  Emission,
  Trend,
  ClimatePlan,
  ApproximatedEmission,
} from './types'

const CLIMATE_DATA_FILE_PATH = path.resolve('./data/output/climate-data.json')

export class ClimateDataService {
  municipalities: Array<Municipality>

  constructor() {
    const climateDataFileContent = fs.readFileSync(CLIMATE_DATA_FILE_PATH, {
      encoding: 'utf-8',
    })
    const jsonData: any[] = JSON.parse(climateDataFileContent)

    this.municipalities = jsonData
      .map((data: any) => {
        const emissions = new Array<EmissionPerYear>()

        Object.entries(data.emissions).forEach(([year, emission]) => {
          const emissionByYear = {
            Year: Number(year),
            CO2Equivalent: emission,
          } as unknown as EmissionPerYear
          emissions.push(emissionByYear)
        })

        const emission = {
          EmissionPerYear: emissions,
          LargestEmissionSectors: new Array<EmissionSector>(),
          HistoricalEmissionChangePercent: data.historicalEmissionChangePercent,
        } as Emission

        const approximatedEmission = {
          TotalCO2Emission: data.totalApproximatedHistoricalEmission,
          EmissionPerYear: Object.entries(data.approximatedHistoricalEmission).map(
            ([year, co2equivalent]) => ({
              Year: Number(year),
              CO2Equivalent: co2equivalent,
            }),
          ),
        } as unknown as ApproximatedEmission

        const trend = {
          TrendCO2Emission: data.trendEmission,
          TrendPerYear: Object.entries(data.trend).map(([year, emissionTrend]) => ({
            Year: Number(year),
            CO2Equivalent: emissionTrend,
          })),
        } as unknown as Trend

        const budget = {
          CO2Equivalent: data.budget,
          BudgetPerYear: Object.entries(data.emissionBudget).map(
            ([year, emissionBudget]) => ({
              Year: Number(year),
              CO2Equivalent: emissionBudget,
            }),
          ),
        } as unknown as Budget

        const climatePlan = {
          Link: data.climatePlanLink,
          YearAdapted: data.climatePlanYear,
          Comment: data.climatePlanComment,
        } as unknown as ClimatePlan

        return {
          Name: data.name,
          HistoricalEmission: emission,
          ApproximatedHistoricalEmission: approximatedEmission,
          EmissionTrend: trend,
          Budget: budget,
          NeededEmissionChangePercent: data.neededEmissionChangePercent,
          HitNetZero: data.hitNetZero,
          BudgetRunsOut: data.budgetRunsOut,
          ElectricCarChangePercent: data.electricCarChangePercent*100,
          ElectricCarChangeYearly: data.electricCarChangeYearly,
          ClimatePlan: climatePlan,
          BicycleMetrePerCapita: data.bicycleMetrePerCapita,
          TotalConsumptionEmission: data.totalConsumptionEmission / 1000,
          ElectricVehiclePerChargePoints: data.electricVehiclePerChargePoints,
          ProcurementScore: data.procurementScore,
          ProcurementLink: data.procurementLink,
        } as Municipality
      })
      .sort(
        (a: Municipality, b: Municipality) => a.HistoricalEmission.HistoricalEmissionChangePercent
          - b.HistoricalEmission.HistoricalEmissionChangePercent,
      )
    this.municipalities.forEach((municipality: Municipality, index: number) => {
      const updatedMunicipality = { ...municipality }
      updatedMunicipality.HistoricalEmission.HistoricalEmissionChangeRank = index + 1
      return updatedMunicipality
    })
  }

  public getMunicipalities(): Array<Municipality> {
    if (this.municipalities.length < 1) {
      throw new Error('No municipalities found')
    }
    return this.municipalities
  }

  public getMunicipality(name: string): Municipality {
    return this.municipalities.filter((kommun) => kommun.Name.toLowerCase() === name)[0]
  }
}
