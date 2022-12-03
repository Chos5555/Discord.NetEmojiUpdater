from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from os import remove

def wrap_in_colon(string):
    # Wrap the input string in colons from both sides
    return ':' + string + ':'


def transform_name(name):
    name = name.replace('-', '_')
    result = list()

    # Create all other variant of emoji if it contains skin tone
    if "skin_tone" in name:
        if "medium_light_skin_tone" in name:
            result.append(wrap_in_colon(name))
            name = name.replace("_medium_light_skin_tone", '')
            result.append(wrap_in_colon(name + "::skin-tone-2"))
            result.append(wrap_in_colon(name + "_tone2"))
        elif "medium_dark_skin_tone" in name:
            result.append(wrap_in_colon(name))
            name = name.replace("_medium_dark_skin_tone", '')
            result.append(wrap_in_colon(name + "::skin-tone-4"))
            result.append(wrap_in_colon(name + "_tone4"))
        elif "light_skin_tone" in name:
            result.append(wrap_in_colon(name))
            name = name.replace("_light_skin_tone", '')
            result.append(wrap_in_colon(name + "::skin-tone-1"))
            result.append(wrap_in_colon(name + "_tone1"))
        elif "medium_skin_tone" in name:
            result.append(wrap_in_colon(name))
            name = name.replace("_medium_skin_tone", '')
            result.append(wrap_in_colon(name + "::skin-tone-3"))
            result.append(wrap_in_colon(name + "_tone3"))
        elif "dark_skin_tone" in name:
            result.append(wrap_in_colon(name))
            name = name.replace("_dark_skin_tone", '')
            result.append(wrap_in_colon(name + "::skin-tone-5"))
            result.append(wrap_in_colon(name + "_tone5"))
        else:
            raise Exception(f"Couldn't find this skin tone, name: {name}")
        # Return result
        return result

    # Else return the name wrapped in colons
    result.append(wrap_in_colon(name))
    return result


def create_current_result(name, value):
    names = transform_name(name)
    result = ""

    # Create result out of names and value
    for curr_name in names:
        result += f"      [\"{curr_name}\"] = \"{value}\",\n"

    return result


def get_emojis(file):
    # Ask user for input
    emoji_url = input("Paste the emojipedia url (e.g. https://emojipedia.org/emoji-13.0/) here or write 'end' if you already did all updates you wanted:")

    # Return if user added all new emojis
    if emoji_url == "end":
        return False

    # Open browser
    browser = webdriver.Chrome()
    browser.get(emoji_url)
    main_window = browser.current_window_handle

    sleep(1)

    # Allow cookies
    browser.find_element(By.XPATH, "//*[@id=\"qc-cmp2-ui\"]/div[2]/div/button[2]").click()

    # Get all newly added emojis
    emoji_list = browser.find_elements(By.XPATH, "/html/body/div[6]/div[1]/article/ul[1]/li")

    result = ""
    cookies = False

    # Do for all new emojis
    for emoji_element in emoji_list:
        # Get name of the emoji
        a_element = emoji_element.find_element(By.TAG_NAME, "a")
        name = a_element.get_attribute("href").split('/')[-2]
        text_name = a_element.text

        # Create emojiterra link
        emojiterra_link = f"https://emojiterra.com/{name}/"

        # Open new window with emojiterra
        browser.execute_script(f"window.open('{emojiterra_link}');")
        new_window = browser.window_handles[-1]

        browser.switch_to.window(new_window)

        # If the cookie accept button hasn't been clicked yet, try to click it
        if not cookies:
            sleep(2)

            try:
                # Allow cookies
                browser.find_element(By.XPATH, "/html/body/div[1]/div/div[4]/div[1]/div[2]/button[4]").click()
                cookies = True
            except:
                pass

            sleep(1)

        # If the emoji wasn't found by the URL and went back to /list, search for it manually by name
        if browser.current_url == "https://emojiterra.com/list/":
            # Remove emojis at the start of the name
            while ord(text_name[0]) not in range(65, 122):
                text_name = text_name[1:]

            # Enter name into searchbox and click enter
            searchbox = browser.find_element(By.XPATH, "//*[@id=\"searchbox\"]")
            searchbox.send_keys(text_name)
            searchbox.send_keys(Keys.ENTER)

            sleep(1)

            # Click the first result
            browser.find_element(By.XPATH, "//*[@id=\"primary\"]/div/a[1]").click()

        # Find JSON value for emoji
        list_of_vals = browser.find_elements(By.XPATH, "//*[@id=\"emoji-codes\"]/tbody/tr")
        for elem in list_of_vals:
            tds =  elem.find_elements(By.TAG_NAME, "td")
            if tds[0].text == "Java, JavaScript & JSON":
                json_value = tds[1].text
                break

        # Create result
        curr_result = create_current_result(name, json_value)
        result += curr_result

        # Close current emoji window and open main one
        browser.close()
        browser.switch_to.window(main_window)

    # Write the result to the file
    file.write(result)

    browser.close()

    return True




def main():
    file_name = "new_emojis.txt"

    # Create new file for new emojis
    file = open(file_name, "w+", encoding="utf8")

    # Add all new emojis
    while get_emojis(file):
        pass

    # Get name of file in which Discord.Net Emojis NamesAndUnicodes is stored
    old_emoji_file_name = input("Input the name of the file with current discord.net emojis:")

    # Open file with old emojis
    old_emoji_file = open(old_emoji_file_name, "r", encoding="utf8")

    # Close and open the file again to reset where the pointer is in the file back to the beggining
    file.close()
    file = open(file_name, "r", encoding="utf8")

    # Get all of the emojis into one list
    old_emojis = old_emoji_file.readlines()
    new_emojis = file.readlines()

    # Put both lists together
    old_emojis.extend(new_emojis)

    # Sort emojis
    old_emojis.sort()

    # Close the file and open it again to write and delete all data in it
    old_emoji_file.close()
    old_emoji_file = open(old_emoji_file_name, "w", encoding="utf8")

    # Write all emojis into the file
    old_emoji_file.writelines(old_emojis)

    # Close files
    old_emoji_file.close()
    file.close()

    # Remove the temporary file
    remove(file_name)


main()