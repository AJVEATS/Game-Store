from main import app
import unittest

# Unit tests for the cloud application
class FlaskTestCase(unittest.TestCase):
    # Ensures that the root page loads correctly
    def test_root(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        print("Root page loads correctly")

    # Ensures that the index page loads correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get("/index", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        print("Index page loads correctly")

    # Ensures that the games page loads correctly
    def test_games(self):
        tester = app.test_client(self)
        response = tester.get("/games", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        print("Games page loads correctly")

    # Ensures that the grand theft auto page game page loads correctly
    def test_game(self):
        tester = app.test_client(self)
        response = tester.get("/animal-crossing-new-horizons", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        print("Game page loads correctly")

    # Ensures that the about us page loads correctly
    def test_about(self):
        tester = app.test_client(self)
        response = tester.get("/about", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        print("About us page loads correctly")

    # Ensures that the store admin page loads correctly
    def test_store_admin(self):
        tester = app.test_client(self)
        response = tester.get("/store-admin", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        print("Store admin page loads correctly")

    # Ensures that the edit games page loads correctly
    def test_edit_games(self):
        tester = app.test_client(self)
        response = tester.get("/edit-games", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        print("Edit games page loads correctly")

    # Ensures that the edit game page loads correctly
    def test_edit_game(self):
        tester = app.test_client(self)
        response = tester.get("/edit-game/animal-crossing-new-horizons", content_type="html/text")
        self.assertEqual(response.status_code, 200)
        print("Edit game page loads correctly")

    # Ensures that the account page loads correctly
    # def test_account(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/account", content_type="html/text")
    #     self.assertEqual(response.status_code, 200)
    #     print("Account page loads correctly")

    # Ensures that the account info page loads correctly
    # def test_account_info(self):
    #     tester = app.test_client(self)
    #     response = tester.get("/account-info", content_type="html/text")
    #     self.assertEqual(response.status_code, 200)
    #     print("Account Info page loads correctly")

    # Ensures that adding a game to the mongoDB works correctly
    def test_add_game(self):
        tester = app.test_client(self)
        response = tester.post(
            "/store-admin",
            data=dict(
                gameSlug="unit-test-game",
                gameName="Unit Test Game",
                gameReleaseDate="2000-01-01",
                gameGenre="Unit Test Genre",
                gameRating="1",
                gameAgeRating="1+",
                gameImage="https://fs-prod-cdn.nintendo-europe.com/media/images/10_share_images/games_15/nintendo_switch_4/H2x1_NSwitch_AnimalCrossingNewHorizons_image1600w.jpg",
                gamePrice="£00.00",
                gameDescription="Unit Test Game Description",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        print("Test game has been added to mongoDB")

    
    # Ensures that deleting a game from the mongoDB works correctly
    def test_delete_game(self):
        tester = app.test_client(self)
        response = tester.delete("/api/game/unit-test-game")
        self.assertEqual(response.status_code, 200)
        print("Test game has been deleted from mongoDB")

    # Ensures that games can only be added with all of the required fields filled
    def test_add_invalid_game(self):
        tester = app.test_client(self)
        response = tester.post(
            "/store-admin",
            data=dict(
                gameSlug="unit-test-game",
                gameReleaseDate="2000-01-01",
                gameGenre="Unit Test Genre",
                gameRating="1",
                gameAgeRating="1+",
                gameImage="https://fs-prod-cdn.nintendo-europe.com/media/images/10_share_images/games_15/nintendo_switch_4/H2x1_NSwitch_AnimalCrossingNewHorizons_image1600w.jpg",
                gamePrice="£00.00",
                gameDescription="Unit Test Game Description",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 400)
        print("Invlaid test game has been rejected")


if __name__ == "__main__":
    unittest.main()
