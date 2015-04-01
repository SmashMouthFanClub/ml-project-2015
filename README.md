### Movie Recommendations Through Streaming and Explicit Rating Data ###
##### Machine Learning Project #####
##### Mike Stowell, Anthony Salani, Misael Moscat #####

#### I. Goal ####

Movie recommendation systems have received a lot of attention as more users turn to services like Netflix and Hulu to watch movies and television series. In 2006, Netflix hosted a competition to create such a machine learning and data mining system. The winners of this competition came up with a solution that utilized a combination of 107 algorithms to improve Netflix’s movie recommendation ratings by 8.43%. Of the 107 algorithms, singular value decomposition contributed the most to this [1].

Our goal is to create a machine learning model that either complements or improves on the problem of movie recommendations. Given a set of users, ratings each user provided for a set of movies, and meta data for each respective movie, we would like to present the user with the top five movie recommendations for him or her. Providing accurate movie recommendations to users will increase user satisfaction and keep them returning to the service. Netflix even reports that 75% of what people watch come from some sort of recommendation [1].

#### II. Motivation ####

Ever since the introduction of streaming services, movie recommendations have become much harder. When users ordered DVDs through websites, they were apt to make more careful decisions, were more likely to view the movie in its entirety, and could not even watch the movie until some time after placing the order to receive the DVD [1]. As a result, users also had to explicitly return to the website to rate the movie. Due to this, it is more likely that a user only goes back to rate this movie if he or she has strong positive or strong negative feelings about it as opposed to relatively neutral. With the introduction of streaming, users are likely to make less optimistic choices that reflect their true interests, may easily click away from the movie, and are much closer to the rating system. With ratings so easily accessible from the movie the user had just finished watching or moved away from, he or she is more likely to provide those more neutral ratings not seen in the case of DVD rentals.

Due to this change in direction for movie viewing, we would like to create a model that works on data that more closely resembles user streaming and rating as opposed to DVD rentals and rating. We aim to test the hypothesis that movie recommendations in this scenario is still possible. Similar papers in the field report varying levels of success, giving us an idea of how to approach the problem [2],[3].

#### III. Approach ####

Our initial approach to solve this problem will be to convert movies each user rated and the tags associated with them into a histogram that attempts to model each user’s preferences. Each histogram will be associated with all of the movies they rated and their rating. This model is subject to change depending on how well it meshes with the chosen means of solving the problem.

We will evaluate several methods of constructing models. An initial survey of existing literature has suggested that k-means clustering and singular value decomposition are useful tools to approach the problem [2]. We will also look into the application of neural networks to this problem. Due to the structure of the data, this approach may be more useful and lead to better results.

Testing our model will be done in several steps. We will first dynamically break down the original dataset into several testing/training subsets and perform cross-validation. The correctness of our model will be determined by using RMSE to determine how closely we match a movie a user watched to what they rated it. However, because recommendation engines have other characteristics that make them useful outside of the correctness of the matches, we will have to measure those as well. For example, novelty of suggestions is important. A food recommendation engine that recommends each user buy bread and milk might be correct, but it is not a novel result.

#### IV. Data Sets ####

The primary dataset that will be used is the MovieLens 10M dataset, which contains 10 million ratings across 10,000 movies. Each rating connects one of the approximately 72,000 users to a handful of movies with a rating between one and five, with intervals of 0.5. The dataset also has about 100,000 tags, which attempt to identify unique features in any given movie that have the potential to be shared with other movies. Examples of tags include “kung fu”, “based on a book”, and “Alfred Hitchcock.” This dataset is entirely user generated and done entirely voluntarily. The website that the MovieLens 10M dataset was obtained from (also named MovieLens) is a site that does not stream movies. Instead, it relies on several thousand volunteers to manually rate and tag each movie.

In the event that the primary dataset fails to construct a functional model for predicting reasonable movie recommendations, we have an alternate dataset with an incredibly similar structure ready. The IMDB dataset, which is a subset of the data on IMDB, contains similar information and could easily replace or extend the MovieLens dataset. In particular, the tags provided by the IMDB dataset could prove to be useful as they are not as oddly specific as the ones in the MovieLens dataset. Also, there are more per movie which increases the likelihood that two similar movies have similar tags.

#### V. Outcome ####

The outcome of this project will be to create a movie recommendation system similar to those used in popular streaming sites such as Netflix or Hulu, which, based on the movie ratings and streaming habits of a user, will recommend relevant content for that user to watch. The proposed system will be able to analyze training data from multiple sources and recognize patterns in movies with similar plots. Using those patterns, along with information from the user, the system will recommend the top five movies for a user to watch. We aim to make progress on the problem of movie recommendations, and by reporting statistics on the success rate of our algorithm, create a system that will be useful for movie watchers and movie makers alike.

#### VI. References ####

1. Amatriain, Xavier, and Justin Basilico. “Netflix Recommendations: Beyond the 5 Stars (Part 1).” The Netflix Tech Blog. Netflix, 6 Apr. 2012. Web.

2. Bystrom, Hans. “Movie Recommendations from User Ratings.” (n.d.): 1-3. CS229 Stanford. Stanford University, 2013. Web.

3. Bao, Zhouxiao, and Haiying Xia. “Movie Rating Estimation and Recommendation.” (n.d.): 1-4. CS229 Stanford. Stanford University, 2012. Web.

#### VII. Other Notes ####

Some code/data based from Andrew Ng's recommender system assignment.
