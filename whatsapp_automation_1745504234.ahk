; Generated on 2025-04-24 14:17:14

; WhatsApp Automation Script Template
; This is the base template used by the automation tool
; Variables enclosed in {variable_name} will be replaced with actual values

; Set custom icon for the script
; Use icon from the app instead of default AutoHotkey icon
#NoEnv
#SingleInstance Force
SetWorkingDir %A_ScriptDir%
SetBatchLines -1
CoordMode, Mouse, Screen

; Sleep time variables (milliseconds)
; These can be adjusted for troubleshooting
global sleep_1 := 1000  ; 1 second
global sleep_2 := 2000  ; 2 seconds
global sleep_3 := 3000  ; 3 seconds
global sleep_4 := 4000  ; 4 seconds

; ========== PHONE NUMBER PROCESSING TEMPLATE ==========
; This block will be repeated for each phone number

; Security check
Sleep {sleep_1}
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep {sleep_2}
Send !{Space}
Send {x}
Sleep {sleep_2}
Send !{d}
Sleep {sleep_1}
Send https://api.whatsapp.com/send/?phone={security_number}
Sleep {sleep_1}
Send {Enter}
Sleep {sleep_3}
MouseMove {coordinate_x},{coordinate_y}, 10
Sleep {sleep_4}
MouseClick, Left, {coordinate_x}, {coordinate_y}
Sleep {sleep_4}
Send +.
Sleep {sleep_4}
Send {Enter}
Sleep {sleep_1}

; Actual phone number messaging
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep {sleep_2}
Send !{Space}
Send {x}
Sleep {sleep_2}
Send !{d}
Sleep {sleep_1}
Send https://api.whatsapp.com/send/?phone={phone_number}
Sleep {sleep_1}
Send {Enter}
Sleep {sleep_4}

; Message Block 1
Sleep {sleep_1}
Send +{message_1}
Sleep {sleep_1}
Send {Enter}

; Message Block 2
Sleep {sleep_1}
Send +{message_2}
Sleep {sleep_1}
Send {Enter}

; Message Block 3
Sleep {sleep_1}
Send +{message_3}
Sleep {sleep_1}
Send {Enter}

; Message Block 4
Sleep {sleep_1}
Send +{message_4}
Sleep {sleep_1}
Send {Enter}

; ========== END PHONE NUMBER PROCESSING TEMPLATE ==========
; Processing phone number 1: 5511948467227

; This block will be repeated for each phone number

; Security check
Sleep 1100
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=5511948467227
Sleep 1100
Send {Enter}
Sleep 3300
MouseMove 700,710, 10
Sleep 4400
MouseClick, Left, 700, 710
Sleep 4400
Send +.
Sleep 4400
Send {Enter}
Sleep 1100

; Actual phone number messaging
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=5511948467227
Sleep 1100
Send {Enter}
Sleep 4400

; Message Block 1
Sleep 1100
Send +Bom dia
Sleep 1100
Send {Enter}

; Message Block 2
Sleep 1100
Send +Este eh um teste
Sleep 1100
Send {Enter}

; Message Block 3
Sleep 1100
Send +Espero que esteja funcionando
Sleep 1100
Send {Enter}

; Message Block 4
Sleep 1100
Send +E tudo corra bem
Sleep 1100
Send {Enter}



; Processing phone number 2: 35679555586

; This block will be repeated for each phone number

; Security check
Sleep 1100
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=5511948467227
Sleep 1100
Send {Enter}
Sleep 3300
MouseMove 700,710, 10
Sleep 4400
MouseClick, Left, 700, 710
Sleep 4400
Send +.
Sleep 4400
Send {Enter}
Sleep 1100

; Actual phone number messaging
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=35679555586
Sleep 1100
Send {Enter}
Sleep 4400

; Message Block 1
Sleep 1100
Send +Ola
Sleep 1100
Send {Enter}

; Message Block 2
Sleep 1100
Send +tudo bem?
Sleep 1100
Send {Enter}

; Message Block 3
Sleep 1100
Send +Vc esta legal?
Sleep 1100
Send {Enter}

; Message Block 4
Sleep 1100
Send +to testando
Sleep 1100
Send {Enter}



; Processing phone number 3: 35677102557

; This block will be repeated for each phone number

; Security check
Sleep 1100
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=5511948467227
Sleep 1100
Send {Enter}
Sleep 3300
MouseMove 700,710, 10
Sleep 4400
MouseClick, Left, 700, 710
Sleep 4400
Send +.
Sleep 4400
Send {Enter}
Sleep 1100

; Actual phone number messaging
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=35677102557
Sleep 1100
Send {Enter}
Sleep 4400

; Message Block 1
Sleep 1100
Send +Opa
Sleep 1100
Send {Enter}

; Message Block 2
Sleep 1100
Send +e ai?
Sleep 1100
Send {Enter}

; Message Block 3
Sleep 1100
Send +testando app
Sleep 1100
Send {Enter}

; Message Block 4
Sleep 1100
Send +vamos ver
Sleep 1100
Send {Enter}



; Processing phone number 4: 35677117768

; This block will be repeated for each phone number

; Security check
Sleep 1100
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=5511948467227
Sleep 1100
Send {Enter}
Sleep 3300
MouseMove 700,710, 10
Sleep 4400
MouseClick, Left, 700, 710
Sleep 4400
Send +.
Sleep 4400
Send {Enter}
Sleep 1100

; Actual phone number messaging
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=35677117768
Sleep 1100
Send {Enter}
Sleep 4400

; Message Block 1
Sleep 1100
Send +EAE
Sleep 1100
Send {Enter}

; Message Block 2
Sleep 1100
Send +certo mano?
Sleep 1100
Send {Enter}

; Message Block 3
Sleep 1100
Send +tmj
Sleep 1100
Send {Enter}

; Message Block 4
Sleep 1100
Send +Vai Corinthians, testando app
Sleep 1100
Send {Enter}



; Processing phone number 5: 5511948467227

; This block will be repeated for each phone number

; Security check
Sleep 1100
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=5511948467227
Sleep 1100
Send {Enter}
Sleep 3300
MouseMove 700,710, 10
Sleep 4400
MouseClick, Left, 700, 710
Sleep 4400
Send +.
Sleep 4400
Send {Enter}
Sleep 1100

; Actual phone number messaging
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=5511948467227
Sleep 1100
Send {Enter}
Sleep 4400

; Message Block 1
Sleep 1100
Send +Bom dia
Sleep 1100
Send {Enter}

; Message Block 2
Sleep 1100
Send +Este eh um teste
Sleep 1100
Send {Enter}

; Message Block 3
Sleep 1100
Send +Espero que esteja funcionando
Sleep 1100
Send {Enter}

; Message Block 4
Sleep 1100
Send +E tudo corra bem
Sleep 1100
Send {Enter}



; Processing phone number 6: 35679555586

; This block will be repeated for each phone number

; Security check
Sleep 1100
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=5511948467227
Sleep 1100
Send {Enter}
Sleep 3300
MouseMove 700,710, 10
Sleep 4400
MouseClick, Left, 700, 710
Sleep 4400
Send +.
Sleep 4400
Send {Enter}
Sleep 1100

; Actual phone number messaging
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=35679555586
Sleep 1100
Send {Enter}
Sleep 4400

; Message Block 1
Sleep 1100
Send +Ola
Sleep 1100
Send {Enter}

; Message Block 2
Sleep 1100
Send +tudo bem?
Sleep 1100
Send {Enter}

; Message Block 3
Sleep 1100
Send +Vc esta legal?
Sleep 1100
Send {Enter}

; Message Block 4
Sleep 1100
Send +to testando
Sleep 1100
Send {Enter}



; Processing phone number 7: 35677102557

; This block will be repeated for each phone number

; Security check
Sleep 1100
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=5511948467227
Sleep 1100
Send {Enter}
Sleep 3300
MouseMove 700,710, 10
Sleep 4400
MouseClick, Left, 700, 710
Sleep 4400
Send +.
Sleep 4400
Send {Enter}
Sleep 1100

; Actual phone number messaging
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=35677102557
Sleep 1100
Send {Enter}
Sleep 4400

; Message Block 1
Sleep 1100
Send +Opa
Sleep 1100
Send {Enter}

; Message Block 2
Sleep 1100
Send +e ai?
Sleep 1100
Send {Enter}

; Message Block 3
Sleep 1100
Send +testando app
Sleep 1100
Send {Enter}

; Message Block 4
Sleep 1100
Send +vamos ver
Sleep 1100
Send {Enter}



; Processing phone number 8: 35677117768

; This block will be repeated for each phone number

; Security check
Sleep 1100
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=5511948467227
Sleep 1100
Send {Enter}
Sleep 3300
MouseMove 700,710, 10
Sleep 4400
MouseClick, Left, 700, 710
Sleep 4400
Send +.
Sleep 4400
Send {Enter}
Sleep 1100

; Actual phone number messaging
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep 2200
Send !{Space}
Send {x}
Sleep 2200
Send !{d}
Sleep 1100
Send https://api.whatsapp.com/send/?phone=35677117768
Sleep 1100
Send {Enter}
Sleep 4400

; Message Block 1
Sleep 1100
Send +EAE
Sleep 1100
Send {Enter}

; Message Block 2
Sleep 1100
Send +certo mano?
Sleep 1100
Send {Enter}

; Message Block 3
Sleep 1100
Send +tmj
Sleep 1100
Send {Enter}

; Message Block 4
Sleep 1100
Send +Vai Corinthians, testando app
Sleep 1100
Send {Enter}


