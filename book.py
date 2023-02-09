import undetected_chromedriver as uc
from tqdm import trange
from rich import print
from stqdm import stqdm
from func_timeout import func_set_timeout, exceptions

class NTUBadmintonCourt:
    def __init__(self, account, password, headless=False, chrome_version=109):
        self.driver = uc.Chrome(headless=headless, version_main=chrome_version) # version change to your chrome version
        self.driver.maximize_window()
        self.account = account
        self.password = password

    def open_badminton_page(self, url='https://sso.wis.ntu.edu.sg/webexe88/owa/sso_login1.asp?t=1&p2=https://wis.ntu.edu.sg/pls/webexe88/srce_smain_s.Notice_O&extra=&pg='):
        self.driver.get(url)
        self.driver.find_element(by='xpath', value='/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[2]/td[2]/input').send_keys(self.account)
        self.driver.find_element(by='xpath', value='/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[4]/td/input[1]').click()
        self.driver.find_element(by='xpath', value='/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[3]/td[2]/input').send_keys(self.password)
        self.driver.find_element(by='xpath', value='/html/body/div/div/div[2]/table/tbody/tr/td/form/center[1]/table/tbody/tr/td/table/tbody/tr[5]/td/input[1]').click()
        self.driver.find_element(by='xpath', value='//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/ul/li[4]/table[2]/tbody/tr[1]/td/input').click() # click badminton

    @func_set_timeout(5) # change according to network
    def wait_string(self, string):
        while True:
            html = self.driver.page_source
            if string in html:
                return html

    def run_epoch(self, button_value):
        # wait for the page to load, if not ready for n seconds, retry  
        try:
            self.wait_string(button_value)
        except:
            print(f"Timed out waiting for {button_value} button")
            return False

        # find the corresponding button and click
        self.driver.find_element(by='xpath', value=f"//input[@value='{button_value}']").click()
        self.wait_string('Confirm')
        self.driver.find_element(by='xpath', value='//*[@id="top"]/div/section[2]/div/div/p/table/tbody/tr/td[2]/form/input[18]').click()
        return True

    def run(self, button_value, max_retry=5):
        for _ in stqdm(trange(max_retry), desc='Try number'):
            if self.run_epoch(button_value):
                print(f"Successfully snap up {button_value}")
                self.driver.quit()
                return True
            # if failed, refresh the page
            self.driver.refresh()

        print(f"Failed to snap up {button_value}")
        self.driver.quit()
        return False

if __name__=='__main__':
    account = ''
    password = ''
    badminton = NTUBadmintonCourt(account, password)
    badminton.open_badminton_page()
    badminton.run(button_value='1BB2BB0117-Feb-20233')
