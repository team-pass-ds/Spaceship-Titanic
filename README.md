<style>
.heading1 {
    color: red;
    font-weight:700;
    font-size: 35px;
}

.header {
  background-image: 'https://images.unsplash.com/photo-1534996858221-380b92700493?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHxr8fGVufDB8fHx8&auto=format&fit=crop&w=1631&q=80'
  width: 100%;
  height: 200px;

}
</style>


<img src="https://images.unsplash.com/photo-1534996858221-380b92700493?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHxr8fGVufDB8fHx8&auto=format&fit=crop&w=1631&q=80" width="100%" height=200px>
# Spaceship Titanic {#identifier .header}

<big>Predict which passengers are transported to an alternate dimension</big>


Welcome to the year 2912, where your data science skills are needed to solve a cosmic mystery. We've received a transmission from four lightyears away and things aren't looking good.

The Spaceship Titanic was an interstellar passenger liner launched a month ago. With almost 13,000 passengers on board, the vessel set out on its maiden voyage transporting emigrants from our solar system to three newly habitable exoplanets orbiting nearby stars.

While rounding Alpha Centauri en route to its first destination—the torrid 55 Cancri E—the unwary Spaceship Titanic collided with a spacetime anomaly hidden within a dust cloud. Sadly, it met a similar fate as its namesake from 1000 years before. Though the ship stayed intact, almost half of the passengers were transported to an alternate dimension!

<img src="https://storage.googleapis.com/kaggle-media/competitions/Spaceship%20Titanic/joel-filipe-QwoNAhbmLLo-unsplash.jpg" width=400>

To help rescue crews and retrieve the lost passengers, you are challenged to predict which passengers were transported by the anomaly using records recovered from the spaceship’s damaged computer system.

Help save them and change history!

### Acknowledgments
Photos by [Joel Filipe](https://unsplash.com/@joelfilip?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText), [Richard Gatley](https://unsplash.com/@uncle_rickie?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) and [ActionVance](https://unsplash.com/@actionvance?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on Unsplash.

### Data Description
In this competition your task is to predict whether a passenger was transported to an alternate dimension during the Spaceship Titanic's collision with the spacetime anomaly. To help you make these predictions, you're given a set of personal records recovered from the ship's damaged computer system.

- `train.csv` - Personal records for about two-thirds (`~8700`) of the passengers, to be used as training data.

|Column|Description|
|:-----|:----------|
|`PassengerId`|A unique Id for each passenger. Each Id takes the form `gggg_pp` where gggg indicates a group the passenger is travelling with and `pp` is their number within the group. People in a group are often family members, but not always.|
|`HomePlanet `|The planet the passenger departed from, typically their planet of permanent residence.|.
|`CryoSleep`|Indicates whether the passenger elected to be put into suspended animation for the duration of the voyage. Passengers in cryosleep are confined to their cabins.|
|`Cabin`|The cabin number where the passenger is staying. Takes the form `deck/num/side`, where side can be either `P` for Port or `S` for Starboard.|
|`Destination`|The planet the passenger will be debarking to.|
|`Age`|The age of the passenger.|
|`VIP`|Whether the passenger had paid for special VIP service during the voyage.|
|`RoomService`, `FoodCourt`, `ShoppingMall`, `Spa`, `VRDeck`|Amount the passenger has billed at each of the Spaceship Titanic's many luxury amenities.|
|`Name`|The first and last names of the passenger.|
|`Transported`|Whether the passenger was transported to another dimension. This is the target, the column you are trying to predict.|

- `test.csv` - Personal records for the remaining one-third (`~4300`) of the passengers, to be used as test data. Your task is to predict the value of `Transported` for the passengers in this set.

- `sample_submission.csv` A submission file in the correct format.
  - `PassengerId` - Id for each passenger in the test set.
  - `Transported` - The target. For each passenger, predict either `True` or `False`.