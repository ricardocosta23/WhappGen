
; WhatsApp Automation Script Template
#NoEnv
#SingleInstance Force
SetWorkingDir %A_ScriptDir%
SetBatchLines -1
CoordMode, Mouse, Screen

; Sleep time variables (milliseconds)
global sleep_1 := 1000  ; 1 second
global sleep_2 := 2000  ; 2 seconds
global sleep_3 := 6000  ; 6 seconds
global sleep_4 := 9000  ; 9 seconds

; ========== PHONE NUMBER PROCESSING TEMPLATE ==========
; Process security number first
Sleep %sleep_1%
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep %sleep_2%
Send !{Space}
Send {x}
Sleep %sleep_2%
Send !{d}
Sleep %sleep_1%
Send https://api.whatsapp.com/send/?phone={security_number}
Sleep %sleep_1%
Send {Enter}
Sleep %sleep_3%
MouseMove {coordinate_x}, {coordinate_y}, 10
Sleep %sleep_4%
MouseClick, Left, {coordinate_x}, {coordinate_y}
Sleep %sleep_4%
Send Security check
Sleep %sleep_4%
Send {Enter}
Sleep %sleep_1%

; Target number part
WinActivate, ahk_exe chrome.exe
WinWaitActive, ahk_exe chrome.exe
Sleep %sleep_2%
Send !{Space}
Send {x}
Sleep %sleep_2%
Send !{d}
Sleep %sleep_1%
Send https://api.whatsapp.com/send/?phone={phone_number}
Sleep %sleep_1%
Send {Enter}
Sleep %sleep_4%

; ========== MESSAGE BLOCKS TEMPLATE ==========
; Messages will be inserted here during script generation
Sleep %sleep_1%
Send {message_text}
Sleep %sleep_1%
Send {Enter}
; ========== END MESSAGE BLOCKS TEMPLATE ==========

; ========== END PHONE NUMBER PROCESSING TEMPLATE ==========
