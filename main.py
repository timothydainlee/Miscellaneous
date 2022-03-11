import time
import numpy as np
from selenium import webdriver


URL = "https://etl.snu.ac.kr"
ID = "ID"
PW = "PW"


if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get(url=URL)
    time.sleep(5)

    # main Login
    driver.find_element_by_id("input-username").send_keys(ID)
    driver.find_element_by_id("input-password").send_keys(PW)
    driver.find_element_by_name("loginbutton").click()
    time.sleep(5)

    # change password page
    if driver.title == "::: Change Password :::":
        driver.find_element_by_name("next_bt").click()

    # get all class information and ask course to complete
    course_elements = driver.find_elements_by_class_name("course-title")
    course_names = [e.find_element_by_tag_name("h3").text for e in course_elements]

    print("\nSelect course.\n")
    for i, n in enumerate(course_names):
        print(f"{i}: {n}")
    input_ = int(input("\nEnter course index: "))
    print(f"Course selected: {course_names[input_]}")
    course_elements[input_].click()
    time.sleep(5)

    # get all VOD information and ask VOD to play
    vod_elements = driver.find_elements_by_class_name("activityinstance")[2:]
    for e in vod_elements:
        ee = e.find_element_by_class_name("instancename")
        v_title, v_class = ee.text.split("\n")

        if v_class != "동영상":
            vod_elements.remove(e)
    vod_names = [e.find_element_by_class_name("instancename").text.split("\n")[0] for e in vod_elements]
    vod_times = [e.find_element_by_class_name("text-info").text[2:] for e in vod_elements]

    vod_names, index = np.unique(vod_names, return_index=True)
    vod_elements = [vod_elements[i] for i in index]
    vod_times = [vod_times[i] for i in index]

    print("\nSelect VODs.\n")
    for i, (n, t) in enumerate(zip(vod_names, vod_times)):
        print(f"{i}: {n}: {t}")
    input_ = input("\nEnter course to complete (space delimited): ")
    input_ = [int(v) for v in input_.split(" ")]

    vod_names = [vod_names[i] for i in input_]
    vod_elements = [vod_elements[i] for i in input_]
    vod_times = [vod_times[i] for i in input_]

    # loop for selected VODs
    for i in range(len(vod_elements)):
        print(f"Playing: {vod_names[i]}: {vod_times[i]}")

        minute, second = vod_times[i].split(":")
        time_ = 60. * int(minute) + int(second) + 5

        # open window, switch scope
        window_before = driver.window_handles[0]
        link = vod_elements[i].find_element_by_tag_name("a").click()
        time.sleep(5)
        
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)

        # click to play
        e = driver.find_element_by_id("vod_player")
        e.click()
        time.sleep(time_)

        # wait, close, switch scope
        driver.close()
        driver.switch_to.window(window_before)

