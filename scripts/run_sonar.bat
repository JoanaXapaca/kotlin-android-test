@echo off
set /p SONAR_TOKEN=<C:\Users\jrego\sonar-token.txt
C:\SonarScanner-8.1.0\sonar-scanner-8.1.0.6389-windows-x64\bin\sonar-scanner.bat -Dsonar.token=%SONAR_TOKEN% -Dsonar.qualitygate.wait=true