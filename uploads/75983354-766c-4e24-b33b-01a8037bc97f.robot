*** Settings ***
Library    SeleniumLibrary
Suite Setup    Open Application Page
Suite Teardown    Close Browser

*** Variables ***
${URL}           https://robot-runner-app.onrender.com/form
${BROWSER}       Chrome
${FIRST_NAME}    Julia
${LAST_NAME}     SnailOps
${EMAIL}         med_execution@gmail.com
${PHONE}         09170000003
${PASSWORD}      SnailPace999
${ADDRESS}       99 Patience Ave
${POSITION}      Project Manager
${GENDER}        Prefer not to say
${START_DATE}    2025-07-25
${RESUME_FILE}   C:/Users/anonu/OneDrive/Desktop/scripts/cinema-tix.pdf


*** Test Cases ***
Medium Execution Time with Delay
    Go To    ${URL}
    Sleep    3s
    Click Button    id=btnProceed    # <-- ito yung landing button

    # Set proper timer value before form starts filling
    Execute JavaScript    document.getElementById('startTime').value = Date.now()

    Wait Until Element Is Visible    id=applicationForm    timeout=10s
    Sleep    3s
    Input Text    id=firstName    ${FIRST_NAME}
    Sleep    3s
    Input Text    id=lastName     ${LAST_NAME}
    Sleep    3s
    Input Text    id=email        ${EMAIL}
    Sleep    3s
    Input Text    id=phone        ${PHONE}
    Input Text    id=password     ${PASSWORD}

    Select From List By Label    id=position    ${POSITION}

    Choose File   id=resume       ${RESUME_FILE}

    Click Button    Submit Application

    Wait Until Page Contains Element    id=successModal    timeout=10s
    Sleep    1s
    Click Button    Continue    # Close modal and show Congrats screen

    Wait Until Page Contains    Congratulations    timeout=10s

*** Keywords ***
Open Application Page
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
