'use strict';

window.addEventListener('load', function () {
    // Redirects the user to the root (/) page when the user signs out
    document.getElementById('sign-out').onclick = function () {
        firebase.auth().signOut();
        window.location.href("/");
    };

    // FirebaseUI config.
    var uiConfig = {
        signInSuccessUrl: '/index',
        signInOptions: [
            firebase.auth.GoogleAuthProvider.PROVIDER_ID,
            firebase.auth.EmailAuthProvider.PROVIDER_ID,
        ]
    };

    firebase.auth().onAuthStateChanged(function (user) {
        if (user) {
            // User is signed in, so it displays the "sign out" button.
            document.getElementById('sign-out').hidden = false;
        } else {
            // User is signed out.
            // Initialize the FirebaseUI Widget using Firebase.
            var ui = new firebaseui.auth.AuthUI(firebase.auth());
            // Shows the Firebase login container.
            ui.start('#firebaseui-auth-container', uiConfig);
            // Hides the sign out button as the user is logged out
            document.getElementById('sign-out').hidden = true;
        }
    }, function (error) {
        console.log(error);
        alert('Unable to log in: ' + error)
    });
});

/**
 *
 * This function gets the slug of the selected game from the store-admin page that the user wants to delete.
 *
 * This function then creates a DELETE API request to the python flask back-end server with the API path
 * '/api/game/' + the slug of the game that the user wants deleted.
 *
 * The if statement gets the status response from the backend. If the status is an error code it sends an
 * alert with the response code status. If the response status code is between 200 and 300 or 4 it end the statement.
 * But if the response status code is not in the range an alert is triggered which displays the error code.
 *
 * @param slug   The slug of the game that the user wants to delete
 *
 */

function deleteGame(slug) {
    // console.log("deleteGame() initiated"); // For Testing
    slug = document.getElementById("delete-game").value;
    //console.log("The usersID is: " + userID); // For Testing
    'use strict';
    const xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/api/game/' + String(slug), true);
    xhr.onload = function () {
        if (xhr.readyState === 4 && xhr.status >= 200 && xhr.status < 300) {

        } else {
            alert("Error " + xhr.status);
        }
    };
    xhr.send();
}

/**
 *
 * This function gets the user id of the user that is currently signed in with firebase authentication and deletes their data that
 * is stored in the applicaitions google datastore.
 *
 * This function then creates a DELETE API request to the python flask back-end server with the API path
 * '/api/userInfo/' + the logged in user's user id.
 *
 * The if statement gets the status response from the backend. If the status is an error code it sends an
 * alert with the response code status. If the response status code is between 200 and 300 or 4 it redirects to the account page (/account).
 * But if the response status code is not in the range an alert is triggered which displays the error code.
 *
 * @param uid   The user id of currently logged in user
 *
 */

function deleteUserInfo(uid) {
    console.log("deleteUserInfo() initiated");
    uid = document.getElementById("uid").value;
    // console.log(uid) // For Testing
    'use strict';
    const xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/api/userInfo/' + String(uid), true);
    xhr.onload = function () {
        if (xhr.readyState === 4 && xhr.status >= 200 && xhr.status < 300) {
            window.location.replace("/account");
        } else {
            alert("Error " + xhr.status);
        }
    };
    xhr.send();
}

/**
 *
 * This function gets the user id of the user that is currently signed in with firebase authentication and the games slug that they have selected
 * to be added to their basket. It then redirects the user to the basket page.
 *
 * This function then creates a POST API request to the python flask back-end server with the API path
 * '/api/addToCart/' + selected games slug + '/' + the logged in user's user id.
 *
 * @param name   The name of the game that the user wants to add to their cart
 * @param price   The price of the game that the user wants to add to their cart
 *
 */

function addToCart(name, price) {

    firebase.auth().onAuthStateChanged(function (user) {
        if (user) {
            let uid = user.uid;
            // console.log("Add to cart initiated with the slug: " + name + " and the user id of " + uid); // For Testing
            console.log(uid);
            console.log(name);
            console.log(price);
            'use strict';
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/api/addToCart/' + String(name) + "/" + String(uid) + "/" + String(price), true);
            xhr.onload = function () {
                if (xhr.readyState === 4 && xhr.status >= 200 && xhr.status < 300) {
                    window.location.replace("/basket");
                } else {
                    alert("Error " + xhr.status);
                }
            };
            xhr.send();
        }
    });
}

/**
 *
 * This function gets the user id of the user that is currently signed in with firebase authentication and the game's name that they have selected
 * to be removed from their basket. It then refreshes the basket page.
 *
 * This function then creates a DELETE API request to the python flask back-end server with the API path
 * '/api/deleteCartItem/' + selected games name + '/' + the logged in user's user id..
 *
 * @param game   The name of the game that the user wants to add to their cart
 * @param uid   The user's userID
 *
 */
function removeFromBasket(game, uid) {
    // console.log("removeFromBasket() function has been initiated"); // For Testing
    // console.log("Passed with the game name " + game); // For Testing
    // console.log("Passed with the uid " + uid); // For Testing
    'use strict';
    const xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/api/deleteCartItem/' + String(game) + '/' + String(uid), true);
    xhr.onload = function () {
        if (xhr.readyState === 4 && xhr.status >= 200 && xhr.status < 300) {
            window.location.replace("/basket");
        } else {
            alert("Error " + xhr.status);
        }
    };
    xhr.send();
}

/**
 *
 * This function gets the user id of the user that is currently signed in with firebase authentication and
 * and clears all games from their basket. It then refreshes the basket page.
 *
 * This function then creates a DELETE API request to the python flask back-end server with the API path
 * '/api/clearBasket/' + the logged in user's user id.
 *
 * @param uid   The user's userID
 *
 */
function clearBasket(uid) {
    console.log("clearBasket() has been initiated"); // For Testing
    console.log("Passed with the uid " + uid); // For Testing
    'use strict';
    const xhr = new XMLHttpRequest();
    xhr.open('DELETE', '/api/clearBasket/' + String(uid), true);
    xhr.onload = function () {
        if (xhr.readyState === 4 && xhr.status >= 200 && xhr.status < 300) {
            window.location.replace("/basket");
        } else {
            alert("Error " + xhr.status);
        }
    };
    xhr.send();
}


/**
 *
 * This function gets the user's games in their basket and then saves the order details in the MongoDB
 * 'Orders' collection. It then refreshes the basket page.
 *
 * This function then creates a POST API request to the python flask back-end server with the API path
 * '/api/purchase/' + the order details object.
 *
 * @param order   The user's order details object
 *
 */
function purchase(order) {
    console.log("purchase() has been initiated");
    console.log(order);
    const order_json = JSON.stringify(order)
    'use strict';
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/api/purchase/' + String(order_json), true);
    xhr.onload = function () {
        if (xhr.readyState === 4 && xhr.status >= 200 && xhr.status < 300) {
            window.location.replace("/orders");
        } else {
            alert("Error " + xhr.status);
        }
    };
    xhr.send();
}