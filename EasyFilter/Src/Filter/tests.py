from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Create your tests here.
class PlayerFormTest(LiveServerTestCase):
    def testVideo(self):
        selenium = webdriver.Chrome(executable_path="C:/chromedriver.exe")
        # urlye yonlendirme
        selenium.get('http://127.0.0.1:8000/')
        # url icindeki etkilesime gecilen elementleri bulma
        words = selenium.find_element_by_id('id_words')
        video = selenium.find_element_by_xpath("//input[@type='file']")

        submit = selenium.find_element_by_id('filter_button')

        file_name = 'sample.mp4'

        # forma veri gonderiyoruz
        words.send_keys('open terminal')
        video.send_keys('c:/users/kuruy/desktop/easyfilterexamples/{}'.format(file_name))


        # formu onayliyoruz
        submit.send_keys(Keys.RETURN)

        selenium.get('http://127.0.0.1:8000/download')

        output_file = selenium.find_element_by_id('output_file')

        output_words = selenium.find_element_by_id('output_words')

        assert 'sample_outputs/{}'.format(file_name) in selenium.page_source
        assert 'open terminal' in selenium.page_source
    

    def testSes(self):
        selenium = webdriver.Chrome(executable_path="C:/chromedriver.exe")
        # urlye yonlendirme
        selenium.get('http://127.0.0.1:8000/')
        # url icindeki etkilesime gecilen elementleri bulma
        words = selenium.find_element_by_id('id_words')
        video = selenium.find_element_by_xpath("//input[@type='file']")

        submit = selenium.find_element_by_id('filter_button')

        file_name = 'sample.flac'

        # forma veri gonderiyoruz
        words.send_keys('open terminal')
        video.send_keys('c:/users/kuruy/desktop/easyfilterexamples/{}'.format(file_name))


        # formu onayliyoruz
        submit.send_keys(Keys.RETURN)

        selenium.get('http://127.0.0.1:8000/download')

        output_file = selenium.find_element_by_id('output_file')

        output_words = selenium.find_element_by_id('output_words')

        assert 'sample_outputs/{}'.format(file_name) in selenium.page_source
        assert 'open terminal' in selenium.page_source
    

    def testFormat(self):
        selenium = webdriver.Chrome(executable_path="C:/chromedriver.exe")
        selenium.get('http://127.0.0.1:8000/')
        # url icindeki etkilesime gecilen elementleri bulma
        words = selenium.find_element_by_id('id_words')
        video = selenium.find_element_by_xpath("//input[@type='file']")

        submit = selenium.find_element_by_id('filter_button')

        file_name = 'yasinkuru_cv.pdf'

        # forma veri gonderiyoruz
        words.send_keys('open terminal')
        video.send_keys('c:/users/kuruy/desktop/easyfilterexamples/{}'.format(file_name))


        # formu onayliyoruz
        submit.send_keys(Keys.RETURN)
        assert 'upload a supported file' in selenium.page_source
    


    def testSure(self):
        selenium = webdriver.Chrome(executable_path="C:/chromedriver.exe")
        selenium.get('http://127.0.0.1:8000/')
        # url icindeki etkilesime gecilen elementleri bulma
        words = selenium.find_element_by_id('id_words')
        video = selenium.find_element_by_xpath("//input[@type='file']")

        submit = selenium.find_element_by_id('filter_button')

        file_name = 'sedat_peker.mp4'

        # forma veri gonderiyoruz
        words.send_keys('open terminal')
        video.send_keys('c:/users/kuruy/desktop/easyfilterexamples/{}'.format(file_name))


        # formu onayliyoruz
        submit.send_keys(Keys.RETURN)
        assert '400 Inline audio exceeds duration limit. Please use a GCS URI.' in selenium.page_source