interface Column {
  Name: string
  Type: string
  DataType: string
  Filters: unknown[] | null
  Value: string
  Unit: null | string
  Description: string
  UniqueId: string
}

interface Header {
  Column: Column[]
  Description: null
}
interface Version {
  Key: Date
  Value: string
}
interface Cell {
  Name: string
  IsMeasure: boolean
  Description: string
  Column: string
  Value: string
  FormattedValue: string
  Level: string
  Gis: string
  UniqueId: string
  NoteIds: number[]
  Versions: Version[]
}

export interface Row {
  Cell: Cell[]
  IsTotal: boolean
}

export interface TrafaResponseObject {
  Header: Header
  Rows: Row[]
  Errors: Error[]
  Description: string
  Name: string
  OriginalName: string
  Notes: { [key: string]: string }
  NextPublishDate: Date
}
