# Stack Exchange Data Explorer SQL Queries:

### Return the number of total posts from the first to the last of the month
- Note: A post is considered anything posted on Stack Overflow this can be a question, answer, or comment.
```
SELECT COUNT(Id)
FROM Posts
WHERE CreationDate BETWEEN '2024-09-01' AND '2024-09-30';
```
### Return the average number of posts per hour of the day from the first to the last of the month
```
SELECT 
    DATEPART(HOUR, CreationDate) AS HourOfDay, 
    ROUND(COUNT(Id) * 1.0 / DATEDIFF(DAY, '2024-09-01', '2024-09-30'), 1) AS AvgPostsPerHour
FROM Posts
WHERE CreationDate BETWEEN '2024-09-01' AND '2024-09-30'
GROUP BY DATEPART(HOUR, CreationDate)
ORDER BY HourOfDay;
```
### Return the number of questions posted from the first to the last of the month
```
SELECT 
    COUNT(Id) AS NumberOfQuestions 
FROM Posts
WHERE CreationDate BETWEEN '2024-09-01' AND '2024-09-30' 
AND ParentId IS NULL;
```
### Return the numner of answers/replies posted from the first to the last of the month
```
SELECT 
    COUNT(Id) AS NumberOfQuestions 
FROM Posts
WHERE CreationDate BETWEEN '2024-09-01' AND '2024-09-30' 
AND ParentId IS NOT NULL;
```
### Returns the average score per question, average view count per question, and average length of body per question posted from the first to the last of the month
```
SELECT 
    AVG(ViewCount) AS AvgViewCountPerPost, 
    AVG(Score) AS AvgScorePerPost, 
    AVG(LEN(Body)) AS AvgLengthOfBodyPerPost
FROM Posts
WHERE CreationDate BETWEEN '2024-09-01' AND '2024-09-30’ 
AND ParentId IS NULL;
```
### Returns the average score per answer, average view count per answer, and average length of body per answer posted from the first to the last of the month
```
SELECT 
    AVG(ViewCount) AS AvgViewCountPerPost, 
    AVG(Score) AS AvgScorePerPost, 
    AVG(LEN(Body)) AS AvgLengthOfBodyPerPost
FROM Posts
WHERE CreationDate BETWEEN '2024-09-01' AND '2024-09-30’ 
AND ParentId IS NOT NULL;
```
### Return the top 20 tags and their usage counts
```
WITH TagCount AS (
    SELECT 
        LTRIM(RTRIM(value)) AS Tag, 
        COUNT(*) AS TagUsageCount
    FROM Posts
    CROSS APPLY STRING_SPLIT(REPLACE(REPLACE(Tags, '<', ''), '>', ' '), ' ') AS SplitTags
    WHERE CreationDate BETWEEN '2024-01-01' AND '2024-01-31'
    GROUP BY LTRIM(RTRIM(value))
)
SELECT TOP 20 
    Tag, 
    TagUsageCount
FROM TagCount
ORDER BY TagUsageCount DESC;
```
### Return the number of accounts created from the first to the last of the month
```
SELECT COUNT(Id) AS AccountsCreated
FROM Users
WHERE CreationDate BETWEEN '2024-01-01' AND '2024-01-31'
```
### Return the number of active users from the first to the last of the month
- Note: An active user is consider to be an individual who has accessed their account at some point in the selected month.
```
SELECT 
    COUNT(Id) AS ActiveUsers
FROM Users
WHERE LastAccessDate BETWEEN '2024-01-01' AND '2024-01-31';
```
### Return the average length of body for a answer from the first to the last of the month
```
SELECT 
    AVG(LEN(Body)) AS AvgBodyLength
FROM Posts
WHERE ParentId IS NOT NULL
AND CreationDate BETWEEN '2024-01-01' AND '2024-01-31';
```
### Return the average highest score for an answer to a Question with atleast 500 views from the first to the last of the month
```
SELECT 
    AVG(p.Score) AS AvgHighestScorePerPost
FROM Posts p
JOIN Posts parentPost ON p.ParentId = parentPost.Id
WHERE p.CreationDate BETWEEN '2018-12-01' AND '2018-12-31'
AND parentPost.ParentId IS NULL
AND parentPost.ViewCount > 500;
```
### Return which tagId represents 'python'
```
SELECT T.Id, T.TagName
FROM Tags AS T
WHERE LOWER(T.TagName) = 'python';
```
### Return which tagId represents 'JavaScript'
```
SELECT T.Id, T.TagName
FROM Tags AS T
WHERE LOWER(T.TagName) = 'javascript';
```
### Return which tagId represents 'Java'
```
SELECT T.Id, T.TagName
FROM Tags AS T
WHERE LOWER(T.TagName) = 'java';
```
### Return the postId type, score, and body of the accepted answer to the top liked posted question created between a given period that have the tags 'python', 'java', or 'javascipt'
```
SELECT 
    PParent.Body AS QuestionBody,
    PAccepted.Score AS AnswerScore,
    PAccepted.Body AS AnswerBody,
    STRING_AGG(T.TagName, ', ') AS QuestionTags  -- Concatenates all tag names with a comma separator
FROM Posts AS PParent
JOIN Posts AS PAccepted ON PParent.AcceptedAnswerId = PAccepted.Id
JOIN PostTags AS PT ON PParent.Id = PT.PostId
JOIN Tags AS T ON PT.TagId = T.Id
WHERE PParent.Id IN (
    SELECT TOP 5 P.Id
    FROM Posts AS P
    JOIN PostTags AS PT ON P.Id = PT.PostId
    WHERE (PT.TagId = 16 OR PT.TagId = 3 OR PT.TagId = 17)  -- Using the tagID for 'python', 'java', 'javascript'
      AND P.CreationDate BETWEEN '2018-12-01' AND '2018-12-31'
      AND P.PostTypeId = 1
    ORDER BY P.Score DESC
)
GROUP BY PParent.Body, PAccepted.Score, PAccepted.Body;
```