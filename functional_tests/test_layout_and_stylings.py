from .base import FunctionalTest


class LayoutSmokeTest(FunctionalTest):

    def test_layout_and_styling(self):

        # Edith goes to the home page
        self.browser.get(self.server_url)
        # the `self.live_server_url` breaks static files
        self.browser.set_window_size(1024, 768)

        # She notices the input box is nicely centered
        inputbox = self.get_item_input_box()

        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=5)

        # she starts a new list and see that the input is nicely
        # centered there too
        inputbox.send_keys('testing\n')
        inputbox = self.get_item_input_box()
        self.assertAlmostEqual(
            inputbox.location['x']+inputbox.size['width']/2,
            512,
            delta=5)
