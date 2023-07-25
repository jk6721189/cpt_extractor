import json
import os
import re
import time
import getpass

# from cptc import cptclist as cptcode
import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.common.by import By

itr = 0
historyText = ""
emca_doc_id: str = ""
audr_doc_id = ""
count = 0
# Export path
direc = "C:\\Users\\"+getpass.getuser()+"\\Desktop\\extracted_data\\"
print(direc)

view_range_xp = "// img[ @ alt = 'View the range page']"
cpt_range_xp = "//td[contains(text(),'Code Section')]"
official_xp = "//td[@title='American Medical Association complete code description.']/following-sibling::td[1]"
consumer_full_name_id = "CCMFullDiv"
consumer_friendly_short_id = "CCMShortDiv"

color_codes_xp = (
    "(//*[contains(text(), 'Color Codes')]/following::td[@class='infobox'][1])[2]"
)
codingtip_id = "(//*[contains(text(), 'Tips')]/following::td[@class='infobox'][1])[1]"
lay_description_xp = "//div[@id='laycode']"
code_specific_reference_information_xp = "(//*[contains(text(), 'Code-Specific Reference Information')]/following::td[@class='infobox'][1])[1]"
# code_range_notes_xp = (
# #     "(//*[contains(text(), 'Code Range Notes')]/following::td[@class='infobox'][1])[1]"
# # )
# code_range_notes_includes_xp = "(//td[@class='cptrangenote']/following-sibling::td)[1]"
# code_range_notes_excludes_xp = "(//td[@class='cptrangenote']/following-sibling::td)[2]"

code_range_notes_includes_xp = "(//td[@class='cptrangenote'])[1]/following-sibling::*[1]"
code_range_notes_excludes_xp = "(//td[@class='cptrangenote'])[2]/following-sibling::*[1]"
code_notes_includes_xp = "(//td[@class='cptrangenote'])[3]/following-sibling::*[1]"
code_notes_excludes_xp = "(//td[@class='cptrangenote'])[4]/following-sibling::*[1]"

code_history_xp = (
    "(//*[contains(text(), 'Code History')]/following::td[@class='infobox'][1])"
)
code_notes_xp = "(//td[@class='cptrangenote']/following-sibling::td)[3]"

url = "https://www.encoderpro.com"

options = webdriver.ChromeOptions()
options.add_argument(
    "user-data-dir=C:\\Users\\"+getpass.getuser()+"\\AppData\\Local\\Google\\Chrome\\Profile"
)
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option(
    "prefs",
    {
        "download.default_directory": "C:\\Users\\"+getpass.getuser()+"\\Desktop\\extracted_data\\",
        # Change default directory for downloads
        "download.prompt_for_download": False,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": False,  # It will not show PDF directly in chrome
    },
)
browser = webdriver.Chrome(
    executable_path="C:\\chromedriver\\chromedriver.exe", chrome_options=options
)

browser.get(url)
time.sleep(10)
browser.maximize_window()
time.sleep(2)
browser.find_element(By.ID, "ohcidSignIn").click()

time.sleep(15)
# print("sleep-15")
browser.find_element(By.ID, 'SignIn').click()
url2 = "https://www.encoderpro.com/epro/cptHandler.do?_k=101*10021&_a=viewDetail"
time.sleep(15)
browser.get(url2)


# cpt_code = browser.current_url.split("*")[1].split("&")[0]

for i in range(10000):
    time.sleep(4)
    try:
        browser.find_element(By.XPATH, view_range_xp).click()
        time.sleep(4)
        cpt_range = str(browser.find_element(By.XPATH, cpt_range_xp).text)
        print("cpt_range",  cpt_range)
        browser.back()
        time.sleep(4)
        pg.hotkey("pageup")
        time.sleep(1)
    except:
        cpt_range = " "
        pass
    try:
        historyText = browser.find_element(By.XPATH, code_history_xp).text
        # print("History: ", historyText)
    except Exception as e:
        print(e)

    try:
        desc_list = []
        official_code = "Official: " + str(
            browser.find_element(By.XPATH, official_xp).text
        ).replace("\n", " ")

        cfn = "Consumer Friendly Full: " + str(
            browser.find_element(By.ID, consumer_full_name_id).text
        ).replace("\n", " ")

        csn = "Consumer Friendly Short: " + str(
            browser.find_element(By.ID, consumer_friendly_short_id).text
        ).replace("\n", " ")

        code_description_data = desc_list.append(official_code)
        desc_list.append(cfn)
        desc_list.append(csn)

    except:
        desc_list = []
        pass

    try:
        color_codes_data = str(
            browser.find_element(By.XPATH, color_codes_xp).text
        ).replace("\n", " ")
    except:
        color_codes_data = " "
        pass

    try:
        codingtip_data = str(browser.find_element(By.XPATH, codingtip_id).text).replace(
            "\n", " "
        )
    except:
        codingtip_data = " "
        pass

    try:
        lay_description_data = str(
            browser.find_element(By.XPATH, lay_description_xp).text
        )
    except:
        lay_description_data = " "
        pass

    try:
        code_specific_reference_information_data_href = str(
            browser.find_element(By.XPATH, code_specific_reference_information_xp).text
        ).replace("\n", " ")
    except:
        code_specific_reference_information_data_href = " "
        pass

    try:
        code_range_notes_includes_data = str(
            browser.find_element(By.XPATH, code_range_notes_includes_xp).text
        ).replace("\n", " ")
    except:
        code_range_notes_includes_data = " "
        pass

    try:
        code_range_notes_excludes_data = str(
            browser.find_element(By.XPATH, code_range_notes_excludes_xp).text
        ).replace("\n", " ")
    except:
        code_range_notes_excludes_data = " "
        pass

    try:
        code_notes_includes_data = str(
            browser.find_element(By.XPATH, code_notes_includes_xp).text
        ).replace("\n", " ")
        if code_notes_includes_data.lower().__contains__('includes'):
            code_notes_includes_data = code_notes_includes_data
    except:
        code_notes_includes_data = " "
        pass

    try:
        code_notes_excludes_data = str(
            browser.find_element(By.XPATH, code_notes_excludes_xp).text
        ).replace("\n", " ")
        if code_notes_excludes_data.lower().__contains__('excludes'):
            code_notes_excludes_data = code_notes_excludes_data
    except:
        code_notes_excludes_data = " "
        pass

    # xpath for tabs - Physician, Facility/OPPS
    # (//td[@valign='bottom'])[]

    tabs = [
        "//table[@id='Physician']//td[1]",
        "//table[@id='Facility/OPPS']//td[1]",
        "//table[@id='MPFS/Medicare']//td[1]",
        "//table[@id='DME/Supply']//td[1]",
        "//table[@id='Ambulance']//td[1]",
        "//table[@id='ASC Modifier']//td[1]",
    ]

    mod_dict = {}
    mods_physician = []
    mods_facility_opps = []
    mods_mpfs_medicare = []
    mods_dme_supply = []
    mods_ambulance = []
    mods_asc_modifier = []
    tab_counter = 0
    try:
        browser.find_element(By.LINK_TEXT, "Modifiers").click()
        time.sleep(4)
        for xpath in tabs:
            tab_counter = tab_counter + 1
            browser.find_element(By.XPATH, xpath).click()
            time.sleep(4)
            if tab_counter == 1:
                for index in range(50):
                    try:
                        data = str(
                            browser.find_element(
                                By.XPATH,
                                f"//table[@id='LIST_BOX_TABLE_ID']/tbody[1]/tr[{index}]/td[2]",
                            ).text
                        )
                        if len(data) > 0:
                            mods_physician.append(data)
                    except:
                        pass
            if tab_counter == 2:
                for index in range(50):
                    try:
                        data = str(
                            browser.find_element(
                                By.XPATH,
                                f"//table[@id='LIST_BOX_TABLE_ID']/tbody[1]/tr[{index}]/td[1]",
                            ).text
                        )
                        if len(data) > 0:
                            mods_facility_opps.append(data)
                    except:
                        pass

            if tab_counter == 3:
                for index in range(50):
                    try:
                        data = str(
                            browser.find_element(
                                By.XPATH,
                                f"//table[@id='LIST_BOX_TABLE_ID']/tbody[1]/tr[{index}]/td[2]",
                            ).text
                        )
                        if len(data) > 0:
                            mods_mpfs_medicare.append(data)
                    except:
                        pass
            if tab_counter == 4:
                try:
                    for index in range(50):
                        try:
                            data = str(
                                browser.find_element(
                                    By.XPATH,
                                    f"//table[@id='LIST_BOX_TABLE_ID']/tbody[1]/tr[{index}]/td[1]",
                                ).text
                            )
                            if len(data) > 0:
                                mods_dme_supply.append(data)
                        except:
                            pass
                except:
                    if len(mods_dme_supply) == 0:
                        mods_dme_supply = []
            if tab_counter == 5:
                try:
                    for index in range(50):
                        data = browser.find_element(
                            By.XPATH,
                            f"//table[@id='LIST_BOX_TABLE_ID']/tbody[1]/tr[{index}]/td[1]",
                        ).text
                        if len(data) > 0:
                            mods_ambulance.append(data)
                except:
                    if len(mods_ambulance) == 0:
                        mods_ambulance = []
            if tab_counter == 6:
                for index in range(50):
                    try:
                        data = str(
                            browser.find_element(
                                By.XPATH,
                                f"//table[@id='LIST_BOX_TABLE_ID']/tbody[1]/tr[{index}]/td[1]",
                            ).text
                        )
                        if len(data) > 0:
                            mods_asc_modifier.append(data)
                    except:
                        pass

        mod_dict = {
            "physician": mods_physician,
            "facility_opps": mods_facility_opps,
            "mpfs_medicare": mods_mpfs_medicare,
            "dme_supply": mods_dme_supply,
            "ambulance": mods_ambulance,
            "asc_modifier": mods_asc_modifier,
        }

        print("mode_dict: ", mod_dict)
        # navigate back to the code page for next code modifier extraction
        browser.back()
        time.sleep(5)

    except:
        pass

    try:
        time.sleep(1)
        browser.find_element(By.CLASS_NAME, "mySlidesEMCA").click()
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[1])
        time.sleep(1)
        browser.get(browser.current_url)
        time.sleep(2)
        # print(browser.current_url)
        emca_doc_id = str(browser.current_url).split("docId=")[1]
        # print(EMCA_DOC_ID)
        time.sleep(1)
        browser.close()
        time.sleep(1)
        browser.switch_to.window(browser.window_handles[0])
    except Exception as e:
        print(e)

    try:
        time.sleep(1)
        try:
            browser.find_element(By.CLASS_NAME, "mySlidesAUDR").click()
        except:
            browser.find_element(By.XPATH, "//img[@class='mySlidesAUDR']").click()
            time.sleep(1)
        browser.switch_to.window(browser.window_handles[1])
        time.sleep(1)
        browser.get(browser.current_url)
        time.sleep(2)
        audr_doc_id = str(browser.current_url).split("docId=")[1]
        # print(AUDR_DOC_ID)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])
    except Exception as e:
        print(e)

    time.sleep(2)
    pg.hotkey("pageup")
    dictionary = {
        "range": cpt_range.split("(")[1].split(")")[0],
        "code_description": desc_list,
        "color_codes": color_codes_data,
        "codingtip": codingtip_data,
        "lay_description": lay_description_data,
        "code_specific_reference_information": code_specific_reference_information_data_href,
        "code_range_notes": "INCLUDES: "
                            + code_range_notes_includes_data
                            + "  EXCLUDES: "
                            + code_range_notes_excludes_data,
        "code_notes": ""
                      + code_notes_includes_data
                      + ""
                      + code_notes_excludes_data,
        "code_history": historyText,
        "emca_doc_id": emca_doc_id,
        "audr_doc_id": audr_doc_id,
        "modifiers": mod_dict,
    }
    # Reset history
    c_range = ""
    historyText = ""
    emca_doc_id = ""
    audr_doc_id = ""
    lay_description_data = ""
    codingtip_data = ""
    color_codes_data = ""
    desc_list = ""
    modifiers = ""

    jsonString = json.dumps(dictionary, indent=4)
    s1 = "\n"
    s2 = " "
    js = re.sub(s1, s2, jsonString)
    # print(jsonString)
    f = open(
        "C:\\Users\\"+getpass.getuser()+"\\Desktop\\extracted_data\\"
        + browser.find_element(By.XPATH, "//*[@class='infoboxTitle']").text
        + "_.json",
        "w",
    )
    for data in js:
        f.write(data)
    f.close()
    time.sleep(1)
    os.system(
        "pprintjson C:\\Users\\"+getpass.getuser()+"\\Desktop\\extracted_data\\"
        + browser.find_element(By.XPATH, "//*[@class='infoboxTitle']").text
        + "_.json >> C:\\Users\\"+getpass.getuser()+"\\Desktop\\extracted_data\\"
        + browser.find_element(By.XPATH, "//*[@class='infoboxTitle']").text
        + ".json"
    )
    try:
        os.remove(
            "C:\\Users\\"+getpass.getuser()+"\\Desktop\\extracted_data\\"
            + browser.find_element(By.XPATH, "//*[@class='infoboxTitle']").text
            + "_.json"
        )
    except:
        # print("File deletion failed.")
        pass

    try:
        time.sleep(5)
        #         scroll = browser.find_element(By.XPATH, "//*[contains(text(),'Medicare Fee')]")
        #         scroll.click()
        #         for _ in range(4):
        #             scroll.send_keys(Keys.PAGE_UP)
        #             time.sleep(.4)
        # time.sleep(2)
        pg.hotkey("pageup")

        time.sleep(2)
        if count == 0:
            time.sleep(5)
            count = 1
        else:
            browser.find_element(
                By.XPATH, "(//div[@id='printAll']//table)[2]/tbody[1]/tr[1]/td[4]"
            ).click()
        time.sleep(10)
    except Exception as e:
        print(f"Exception {e}")
        print("Next page navigation failed.")
