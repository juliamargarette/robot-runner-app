*** Settings ***
Library           SeleniumLibrary
Library           sys    WITH NAME    sys
Suite Setup       Setup Headless Browser
Suite Teardown    Close Browser

*** Variables ***
${URL}           https://robot-runner-app.onrender.com/form
${FIRST_NAME}    Julia
${LAST_NAME}     SnailOps
${EMAIL}         med_execution@gmail.com
${PHONE}         09170000003
${PASSWORD}      SnailPace999
${ADDRESS}       99 Patience Ave
${POSITION}      Project Manager
${GENDER}        Prefer not to say
${START_DATE}    2025-07-25
# For file upload, use a relative path within the project if you re-enable Choose File
${RESUME_FILE}   uploads/cinema-tix.pdf

*** Keywords ***
Setup Headless Browser
    ${options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys
    Call Method    ${options}    add_argument    --headless
    Call Method    ${options}    add_argument    --no-sandbox
    Call Method    ${options}    add_argument    --disable-dev-shm-usage

    ${service}=    Evaluate    sys.modules['selenium.webdriver.chrome.service'].Service(executable_path='chromedriver/chromedriver')    sys

    Create WebDriver    Chrome    options=${options}    service=${service}
    Go To    ${URL}
    Maximize Browser Window

*** Test Cases ***
Medium Execution Time with Delay
    Sleep    6s
    Click Button    id=btnProceed

    Execute JavaScript    document.getElementById('startTime').value = Date.now()

    Wait Until Element Is Visible    id=applicationForm    timeout=10s
    Sleep    6s
    Input Text    id=firstName    ${FIRST_NAME}
    Sleep    6s
    Input Text    id=lastName     ${LAST_NAME}
    Sleep    6s
    Input Text    id=email        ${EMAIL}
    Sleep    6s
    Input Text    id=phone        ${PHONE}
    Input Text    id=password     ${PASSWORD}

    Select From List By Label    id=position    ${POSITION}

    Wait Until Element Is Visible    id=btnSubmit    timeout=10s
    Scroll Element Into View         id=btnSubmit

    # Choose File step (optional – enable only if applicable)
    # Choose File    id=resume    ${RESUME_FILE}

    Click Button    id=btnSubmit

    Wait Until Page Contains Element    id=successModal    timeout=10s
    Sleep    6s
    Click Button    Continue

    Sleep    6s
    Wait Until Page Contains    Congratulations    timeout=10s
