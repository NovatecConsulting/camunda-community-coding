param(
[string]$url
)

"ngrok url: $url"
"setting new url for aufgaben_anna"
cd aufgaben_anna
$string = Get-Content ".\lambda\lambda_function.py"
$string[26] = "camunda_url = `"$url`""
$string[26]
$string | Set-Content ".\lambda\lambda_function.py"
git stage ".\lambda\lambda_function.py"
git commit -m "ngrok url updated"
git push
ask deploy
cd ..
"setting new url for aufgaben_felix"
cd aufgaben_felix
$string = Get-Content ".\lambda\lambda_function.py"
$string[26] = "camunda_url = `"$url`""
$string[26]
$string | Set-Content ".\lambda\lambda_function.py"
git stage ".\lambda\lambda_function.py"
git commit -m "ngrok url updated"
git push
ask deploy
cd ..
"setting new url for aufgaben_julian"
cd aufgaben_julian
$string = Get-Content ".\lambda\lambda_function.py"
$string[26] = "camunda_url = `"$url`""
$string[26]
$string | Set-Content ".\lambda\lambda_function.py"
git stage ".\lambda\lambda_function.py"
git commit -m "ngrok url updated"
git push
ask deploy
cd ..
"setting new url for meine_bestellung"
cd meine_bestellung
$string = Get-Content ".\lambda\lambda_function.py"
$string[26] = "camunda_url = `"$url`""
$string[26]
$string | Set-Content ".\lambda\lambda_function.py"
git stage ".\lambda\lambda_function.py"
git commit -m "ngrok url updated"
git push
ask deploy
cd ..
"setting new url for manager-hotel-karlsruhe"
cd manager-hotel-karlsruhe
$string = Get-Content ".\lambda\lambda_function.py"
$string[26] = "camunda_url = `"$url`""
$string[26]
$string | Set-Content ".\lambda\lambda_function.py"
git stage ".\lambda\lambda_function.py"
git commit -m "ngrok url updated"
git push
ask deploy
cd ..
"done, all set"