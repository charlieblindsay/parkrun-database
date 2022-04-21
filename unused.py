def get_postcode(driver, parkrun_name):
    park_name = parkrun_name[:-3]

    search_text = f'{park_name} post code'

    driver.get('https://www.google.com/')

    driver.find_element_by_xpath('//*[@id="L2AGLb"]').click()

    google_search_input_field = driver.find_element(by=By.NAME, value='q')
    google_search_input_field.send_keys(search_text)
    google_search_input_field.send_keys(Keys.RETURN)

    urls = [anchor.get_attribute('href') for anchor in driver.find_elements(
        by=By.CSS_SELECTOR, value='div > a')]

    output = ''
    blacklist = [
        '[document]',
        'noscript',
        'html',
        'meta',
        'head',
        'input',
        'script',
    ]

    for url in urls:
        if url != None and re.search(r'google', str(url)) == None:
            res = requests.get(url)
            html_page = res.content
            soup = BeautifulSoup(html_page, 'html.parser')
            text = soup.find_all(text=True)
            for t in text:
                output += '{} '.format(t)
            if output != '':
                break

    postcode_format_regex_list = [
        r'[A-Z]{2}[0-9]{1}[A-Z]{1}\s[0-9]{1}[A-Z]{2}',
        r'[A-Z]{1}[0-9]{1}[A-Z]{1}\s[0-9]{1}[A-Z]{2}',
        r'[A-Z]{1}[0-9]{1}\s[0-9]{1}[A-Z]{2}',
        r'[A-Z]{1}[0-9]{2}\s[0-9]{1}[A-Z]{2}',
        r'[A-Z]{2}[0-9]{1}\s[0-9]{1}[A-Z]{2}',
        r'[A-Z]{2}[0-9]{2}\s[0-9]{1}[A-Z]{2}']

    print(output)

    for postcode_format in postcode_format_regex_list:
        if re.search(postcode_format, output):
            parkrun_postcode = re.search(
                '[A-Z]{2}[0-9]{2}\s[0-9]{1}[A-Z]{2}', output)[0]
            print(f'Park run: {parkrun_name}, Postcode: {parkrun_postcode}')

            return parkrun_postcode
        else:
            return 'Postcode not found'
