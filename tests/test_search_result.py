from pages.home_page import HomePage
from pages.search_result import SearchPage
import logging

logger = logging.getLogger("TestSearchResult")

class TestSearchResult:
    def test_search_hotel_in_bangalore(self, driver):
        home_page = HomePage(driver)
        search_page = SearchPage(driver)
        home_page.close_login_popup()
        home_page.tap_hotels_tab()
        home_page.click_search_field()
        home_page.enter_search_text("Bangalore")
        home_page.select_first_suggestion()
        home_page.select_tomorrow_date()
        home_page.tap_search_button()
        search_page.close_popup()
        results = search_page.get_search_results("Bangalore")
        assert results, "No search results found for Bangalore."
        logger.info("Search results for Bangalore validated successfully.")
