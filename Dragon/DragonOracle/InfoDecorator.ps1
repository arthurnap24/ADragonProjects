param(
    $symbolsByRsi = @{40 = @("CPRI")}
)

$supportResistantStopLossDivClass = "D(ib) Va(m) Mstart(30px) Fz(s)"

$symbolsByRsi.Keys | ForEach-Object {
    $symbolsByRsi[$_] | ForEach-Object {
        # Append the symbol to the chart url, Yahoo Finance will fill the rest
        $yahooChartURL = "https://finance.yahoo.com/chart/$_"
        $webResponse = Invoke-WebRequest $yahooChartURL -UseBasicParsing
    }
}