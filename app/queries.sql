-- Active: 1744365292504@@127.0.0.1@5432@quiz


    

select * from answertable;

select *
from
    questionnairetable
    join answerstable on answerstable.questionnaire_id = questionnairetable.id
    join answertable on answertable.answers_id = answerstable.id
    where answerstable.user_id = 'f0297956-f2e2-4acf-90b5-28f4067d4b78' and questionnairetable.id = '3cc5f35d-edee-4351-ac39-326e008ec952'


/*
 Get total no.of participants per questionnaire
*/
SELECT
    count(answerstable.id), answerstable.questionnaire_id
from answerstable
join questionnairetable on questionnairetable.id = answerstable.questionnaire_id
GROUP BY answerstable.questionnaire_id;


/*
Get total no.of participant count on a particular questionnaire
*/
SELECT
    *
FROM answerstable
join questionnairetable on questionnairetable.id = answerstable.questionnaire_id
where answerstable.questionnaire_id = '536eeb30-7b39-41a3-abe0-9d04587cd6a4';

/*
Get answers of the participants of a particular questionnaire
*/
SELECT
    *
from answertable
join answerstable on answerstable.id = answertable.answers_id
join questionnairetable on  
