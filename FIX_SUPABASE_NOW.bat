@echo off
echo ========================================
echo FIXING SUPABASE DNS FOR INDIA
echo ========================================
echo.

echo Step 1: Flushing DNS cache...
ipconfig /flushdns

echo.
echo Step 2: Testing current DNS resolution...
nslookup db.tmavkmymbdcmugunjtle.supabase.co

echo.
echo Step 3: Adding Google DNS to hosts file...
echo 76.76.21.21 db.tmavkmymbdcmugunjtle.supabase.co >> C:\Windows\System32\drivers\etc\hosts

echo.
echo Step 4: Flushing DNS again...
ipconfig /flushdns

echo.
echo Step 5: Testing connection...
ping db.tmavkmymbdcmugunjtle.supabase.co -n 2

echo.
echo ========================================
echo DNS FIX COMPLETE!
echo Now restart your backend server
echo ========================================
pause
