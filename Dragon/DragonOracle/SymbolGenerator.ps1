param(
    $outputLinksFilesDir = $null,
    $limitRsi = 20,
    $mailAddress = ""
)

$terminalName = "Windows"
try {
    foreach ($entry in (Get-ChildItem -Path Env:)) { 
        if ($entry.Name -eq "TERM") {
            Write-Host "Hello"
            $terminalName = $entry.Value
        }
    }
    # Must be a Unix operating system, unless PowerShell can also be ran by other OS
    if ($terminalName -ne "Windows") {
        Write-Host "Not a Windows operating system... "
    }
}
catch {
    Write-Host "Cannot find operating system, defaulting to Windows."
    $terminalName = "Windows"
}

Add-Type -AssemblyName System.Drawing

# Source: https://community.idera.com/database-tools/powershell/powertips/b/tips/posts/converting-text-to-image
function Convert-TextToImage
{
  param
  (
    [String]
    [Parameter(Mandatory)]
    $Text,
    
    [String]
    $Font = 'Consolas',
    
    [ValidateRange(5,400)]
    [Int]
    $FontSize = 24,
    
    [System.Windows.Media.Brush]
    $Foreground = [System.Windows.Media.Brushes]::Black,
    
    [System.Windows.Media.Brush]
    $Background = [System.Windows.Media.Brushes]::White
  )
  
  $filename = "$env:temp\$(Get-Random).png"

  # take a simple XAML template with some text  
  $xaml = @"
<TextBlock
   xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
   xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml">$Text</TextBlock>
"@

  Add-Type -AssemblyName PresentationFramework
  
  # turn it into a UIElement
  $reader = [XML.XMLReader]::Create([IO.StringReader]$XAML)
  $result = [Windows.Markup.XAMLReader]::Load($reader)
  
  # refine its properties
  $result.FontFamily = $Font
  $result.FontSize = $FontSize
  $result.Foreground = $Foreground
  $result.Background = $Background
  
  # render it in memory to the desired size
  $result.Measure([System.Windows.Size]::new([Double]::PositiveInfinity, [Double]::PositiveInfinity))
  $result.Arrange([System.Windows.Rect]::new($result.DesiredSize))
  $result.UpdateLayout()
  
  # write it to a bitmap and save it as PNG
  $render = [System.Windows.Media.Imaging.RenderTargetBitmap]::new($result.ActualWidth, $result.ActualHeight, 96, 96, [System.Windows.Media.PixelFormats]::Default)
  $render.Render($result)
  Start-Sleep -Seconds 1
  $encoder = [System.Windows.Media.Imaging.PngBitmapEncoder]::new()
  $encoder.Frames.Add([System.Windows.Media.Imaging.BitmapFrame]::Create($render))
  $filestream = [System.IO.FileStream]::new($filename, [System.IO.FileMode]::Create)
  $encoder.Save($filestream)
  
  # clean up
  $reader.Close() 
  $reader.Dispose()
  
  $filestream.Close()
  $filestream.Dispose()
  
  # return the file name for the generated image
  $filename 
}

$symbolHTMLClass = "screener-link-primary"
$tabLink = "tab-link"

# Possible rsi values from the drop-down
$rsiLimitSymbolsMap = @{
    10=@();
    20=@();
    30=@();
    40=@();
    50=@();
    60=@();
    70=@();
    80=@();
    90=@();
}


# Get the symbols from the screener results from finviz

$rsiRange = @(10, 20, 30, 40, 50, 60, 70, 80, 90)
$rsis = @()
foreach ($rsi in $rsiRange) {
    if ($rsi -le $limitRsi) {
        $rsis += $rsi
    }
    else {
        break;
    }
}
$rsis | Foreach-Object {
    # Save the rsi to be used inside the pipeline operations
    $rsi = $_
    $finvizUrlPrefix = "https://finviz.com"
    $originalUrl = "$finvizurlPrefix/screener.ashx?v=111&f=sh_avgvol_o1000,ta_rsi_os$rsi&ft=3&o=rsi"
    $finvizScreenerURL = "$finvizurlPrefix/screener.ashx?v=111&f=sh_avgvol_o1000,ta_rsi_os$rsi&ft=3&o=rsi"

    Write-Host -ForegroundColor Green "Gathering symbols with RSI = $rsi"

    $shouldContinue = $true
    # Write-Host "rsi is $rsi"
    while ($shouldContinue) {
        Write-Host "  ...using url $finvizScreenerURL"
        $shouldContinue = $false
        $webResponse = (Invoke-WebRequest -Uri $finvizScreenerURL)
        $webResponseLinks = $webResponse.Links
        foreach ($link in $webResponseLinks) {
            if ($link.class -eq $symbolHTMLClass) {
                if ($terminalName -eq "Windows") {
                    $symbol = $link.innerHTML
                }
                else {
                    # PowerShell for Mac does not have the innerHtml property built in
                    $symbol = $link.outerHTML.Replace(' ', '').Split('<').Split('>')[2]
                }

                # if symbol is found in the rsis before, don't include it
                $rsiLimitSymbolsMap[$rsi] += $symbol
                Write-Host "    ...Adding $symbol to RSI = $rsi bin"
            }
            if ($link.class -eq $tabLink) {
                if ($link.innerText -eq "next") {
                    Write-Host "      ...Next button found, gathering more symbols with RSI = $rsi"
                    # repeat the logic until there's no more next button
                    $shouldContinue = $true
                    $href = "$finvizUrlPrefix/$($link.href)"
                    $pageParam = ($href -split ';')[-1]
                    $finvizScreenerURL = "$originalUrl&$pageParam"
                }
            }
        }
    }
}

Write-Host -ForegroundColor Green "Finished gathering all symbols, storing results to a file with their charts' links to YahooFinance."

if (!$outputLinksFilesDir) {
    if ($terminalName -ne "Windows") {
        $outputLinksFilesDir = "\Dragon\LinksFiles"
    }
    else {
        $outputLinksFilesDir = "C:/Dragon/LinksFiles"
    }
    
    Write-Host "No outputLinksFilesDir parameter supplied, defaulting to $outputLinksFilesDir"
}

$outputLinksFileName = "$(Get-Date -Format `"yyyy-MM-dd`").html"
$outputLinksFile = Join-Path $outputLinksFilesDir $outputLinksFileName
if (!(Test-Path -Path $outputLinksFilesDir -ErrorAction SilentlyContinue)) {
    Write-Host -ForegroundColor Yellow "$outputLinksFilesDir does not exist, creating..."
    New-Item -Path "$outputLinksFilesDir" -ItemType "directory" -Force
    if (Test-Path -Path $outputLinksFilesDir -ErrorAction SilentlyContinue) {
        Write-Host -ForegroundColor Green "  Successfully created $outputLinksFilesDir"
    }
    else {
        Write-Host -ForegroundColor Red "  Failed to create $outputLinksFilesDir"
    }
}
else {
    Write-Host -ForegroundColor Green "$outputLinksFilesDir exists, creating symbols links file and storing there."
}

if (Test-Path $outputLinksFile -ErrorAction SilentlyContinue) {
    Write-Host "symbols links file already exists, recreating..."
    Remove-Item -Path $outputLinksFile
}

# Output the symbols in to a file as a side effect

# Pass the symbols to HtmlFileGenerator.ps1

# Have Dragon Orchestrator run all of these together via psake???

# Linkify and output results to a file with date, shove it in S3 or something


$keys = $rsiLimitSymbolsMap.Keys | sort
$sortedKeyInt = @()
foreach($key in $keys) {
    $sortedKeyInt += [int]$key   
}

foreach ($rsi in $sortedKeyInt) {
    $rsiHeader = "<h4>[RSI = $rsi]</h4>"
    $symbols = $rsiLimitSymbolsMap[$rsi]

    # If the symbol list is empty, then don't output the rsi
    if ($symbols.Count -lt 1) {
        continue;
    }
    Write-Host -ForegroundColor Green "Appending symbols with rsi = $rsi to $outputLinksFile"

    for ($i = 0; $i -lt $symbols.Count; $i++) {
        $symbol = $symbols[$i]
        $symbols[$i] = "<a href=https://finance.yahoo.com/chart/$symbol>$symbol</a></br>"
    } 
    $symbols = $symbols | Out-String
    $rsiHeader | Out-File -Append $outputLinksFile
    $symbols | Out-File -Append $outputLinksFile
}

# Email the file if specified
if ($mailAddress) {
    Write-Host -ForegroundColor Green "Finished writing symbol links to a file, sending as an email to: "
}