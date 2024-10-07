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
    COUNT(Id) AS NumberOfQuestions, 
FROM Posts
WHERE CreationDate BETWEEN '2024-09-01' AND '2024-09-30' 
AND ParentId IS NULL;
```
### Returns the average score per question, average view count per question, and average length of the question posted from the first to the last of the month
```
SELECT 
    AVG(ViewCount) AS AvgViewCountPerPost, 
    AVG(Score) AS AvgScorePerPost, 
    AVG(LEN(Body)) AS AvgLengthOfBodyPerPost
FROM Posts
WHERE CreationDate BETWEEN '2024-09-01' AND '2024-09-30’ 
AND ParentId IS NULL;
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
