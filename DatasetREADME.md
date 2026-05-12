CLEANED DATASET: https://drive.google.com/file/d/1AQlcVhxlIzkKxJ2JAFSRLjvf_56KAEC8/view?usp=sharing

timestamp - when interaction happened / when student studied
solving_id - likely student/session identifier
question_id - question attempted
user_answer - student answer
elapsed_time -  time spent

We CANNOT see: videos, pictures, audio, animations
So the dataset never tells us directly: "This student watched multimedia".
Since KT1 has no video information,we use: time spent + number of interactions to guess engagement.

STEP 1 — Count how long each student stayed
STEP 2 — Count how many questions each student did
STEP 3 — Combine both Long time + many questions = higher engagement
STEP 4 — Decide who is highly engaged
You are NOT saying: "This student watched videos" ,because KT1 does not show videos.
But Rather you are saying: "This student behaved like an engaged learner" using: time spent and number of activities

The engineered features allow the project to analyze student learning behavior using interaction-based proxies for engagement and performance.
Feature	                  Simple Meaning
performance_gain     	how active student is
day              	which day activity happened
year            	which year activity happened
