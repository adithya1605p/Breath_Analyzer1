# Fix DNS to access Supabase in India
# Run as Administrator

Write-Host "Fixing DNS to access Supabase..." -ForegroundColor Green

# Get active network adapter
$adapter = Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | Select-Object -First 1

if ($adapter) {
    Write-Host "Found adapter: $($adapter.Name)" -ForegroundColor Yellow
    
    # Set DNS to Google DNS (8.8.8.8 and 8.8.4.4)
    Set-DnsClientServerAddress -InterfaceIndex $adapter.ifIndex -ServerAddresses ("8.8.8.8","8.8.4.4")
    
    Write-Host "DNS changed to Google DNS (8.8.8.8, 8.8.4.4)" -ForegroundColor Green
    Write-Host "Flushing DNS cache..." -ForegroundColor Yellow
    
    # Flush DNS cache
    ipconfig /flushdns
    
    Write-Host "Testing Supabase connection..." -ForegroundColor Yellow
    Test-Connection -ComputerName db.tmavkmymbdcmugunjtle.supabase.co -Count 2
    
    Write-Host "`nDNS fix complete! Restart your backend now." -ForegroundColor Green
} else {
    Write-Host "No active network adapter found!" -ForegroundColor Red
}
