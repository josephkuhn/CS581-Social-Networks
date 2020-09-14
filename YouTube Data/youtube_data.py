# Author: Joseph Kuhn

#  youtube_data.py searches YouTube for videos matching a search term
#  It writes info for each video, up to a specified maximum number, to a .csv file
#  It will also determine which videos from the searched list have the greatest amount of likes, dislikes, comments, and views,
#  as well as the highest like/dislike ratio. From this data, it will determine if one video stands out as the most popular,
#  and it will tell the user which video this is, if any.

# to run from terminal window:  
#      python3 youtube_data.py --search_term mysearch --search_max mymaxresults
#  where:  search_term = the term you want to search for;  default = music
#     and  search_max = the maximum number of results;  default = 30
# For example: python3 youtube_data.py --search_term fish --search_max 20

from apiclient.discovery import build      # use build function to create a service object

import argparse    #  need for parsing the arguments in the command line
import csv         #  need since search results will be contained in a .csv file
import unidecode   #  need for processing text fields in the search results

# put your API key into the API_KEY field below, in quotes
API_KEY = "AIzaSyAlrnAMBhQ8RJ8xXpXKnBNOAFGImooe_uQ"

API_NAME = "youtube"
API_VERSION = "v3"       # this should be the latest version

# sets up a bunch of variables to store video data
maxViews = 0
maxViewsTitle = "N/A"
maxLikes = 0
tempLikes = 0
maxLikesTitle = "N/A"
maxDislikes = 0
tempDislikes = 0
maxDislikesTitle = "N/A"
maxLikeDislikeRatio = 0
maxLikeDislikeRatioTitle = "N/A"
maxComments = 0
tempComments = 0
maxCommentsTitle = "N/A"
mostPopularTitle = "N/A"

tempPoints = 0

popularVideos = {} # sets up a dictionary to store the popular videos

#  function youtube_search retrieves the YouTube records

def youtube_search(options):
    youtube = build(API_NAME, API_VERSION, developerKey=API_KEY)
    
    search_response = youtube.search().list(q=options.search_term, part="id,snippet", maxResults=options.search_max).execute()
    
    # create a CSV output for results video list, and write the headings line
    csvFile = open('video_results.csv','w')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(["TITLE","ID","VIEWS","LIKES","DISLIKES","COMMENTS","FAVORITES", "LIKE/DISLIKE RATIO"])

    global tempPoints, maxViews, maxViewsTitle, maxLikes, maxLikesTitle, maxDislikes, maxDislikesTitle, tempLikes, tempDislikes, maxLikeDislikeRatio, maxLikeDislikeRatioTitle, maxComments, maxCommentsTitle, mostPopularTitle, tempComments

    # search for videos matching search term; write an output line for each
    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)  
            videoId = search_result["id"]["videoId"]
            video_response = youtube.videos().list(id=videoId,part="statistics").execute()
            for video_results in video_response.get("items",[]):
                viewCount = video_results["statistics"]["viewCount"]
                viewCount = int(viewCount)
                if viewCount > maxViews:
                    maxViews = viewCount
                    maxViewsTitle = title
                if 'likeCount' not in video_results["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_results["statistics"]["likeCount"]
                    tempLikes = int(likeCount) # store likes for the ratio
                    likeCount = int(likeCount)
                    if likeCount > maxLikes: # check which video has the most likes
                        maxLikes = likeCount
                        maxLikesTitle = title
                if 'dislikeCount' not in video_results["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_results["statistics"]["dislikeCount"]
                    tempDislikes = int(dislikeCount) # store dislikes for the ratio
                    dislikeCount = int(dislikeCount)
                    if dislikeCount > maxDislikes: # check which video has the most dislikes
                        maxDislikes = dislikeCount
                        maxDislikesTitle = title
                if 'commentCount' not in video_results["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_results["statistics"]["commentCount"]
                    commentCount = int(commentCount)
                    if commentCount > maxComments: # check which video has the most comments
                        maxComments = commentCount
                        maxCommentsTitle = title
                if 'favoriteCount' not in video_results["statistics"]:
                    favoriteCount = 0
                else:
                    favoriteCount = video_results["statistics"]["favoriteCount"]
            tempLikeDislikeRatio = tempLikes / tempDislikes # save this value for the csv file
            if tempLikeDislikeRatio > maxLikeDislikeRatio: # find the video with the highest like/dislike ratio
                maxLikeDislikeRatio = tempLikeDislikeRatio
                maxLikeDislikeRatioTitle = title
            csvWriter.writerow([title,videoId,viewCount,likeCount,dislikeCount,commentCount,favoriteCount,tempLikeDislikeRatio])

    csvFile.close()
  
# main routine
parser = argparse.ArgumentParser(description='YouTube Search')
parser.add_argument("--search_term", default="music")
parser.add_argument("--search_max", default=30)
args = parser.parse_args()
print("Search term: " + args.search_term)
print("Maximum search results: " + args.search_max)
    
youtube_search(args)

if maxViewsTitle in popularVideos:
    popularVideos[maxViewsTitle] += 1 # if the title already exists in the dictionary, increment the value
else:
    popularVideos[maxViewsTitle] = 1 # if not, create it

if maxLikesTitle in popularVideos:
    popularVideos[maxLikesTitle] += 1
else:
    popularVideos[maxLikesTitle] = 1

if maxLikeDislikeRatioTitle in popularVideos:
    popularVideos[maxLikeDislikeRatioTitle] += 1
else:
    popularVideos[maxLikeDislikeRatioTitle] = 1

if maxCommentsTitle in popularVideos:
    popularVideos[maxCommentsTitle] += 1
else:
    popularVideos[maxCommentsTitle] = 1

maxVideoValue = 0
maxVideoValueTitle = "N/A"

for name, value in popularVideos.items(): # iterate through the dictionary and find the video with the highest popularity value
    if value > maxVideoValue:
        maxVideoValue = value
        maxVideoValueTitle = name

for name, value in popularVideos.items(): # confirm that there aren't two or more videos with the same popularity value
    if name == maxVideoValueTitle:
        continue
    if value == maxVideoValue:
        maxVideoValue = 0

print("The video with the most views is \"" + maxViewsTitle + "\" with " + str(maxViews) + " views.")
print("")
print("The video with the most likes is \"" + maxLikesTitle + "\" with " + str(maxLikes) + " likes.")
print("")
print("The video with the most dislikes is \"" + maxDislikesTitle + "\" with " + str(maxDislikes) + " dislikes.")
print("")
if maxLikeDislikeRatio == 1:
    print("The video with the best like/dislike ratio is \"" + maxLikeDislikeRatioTitle + "\". It has approximately " + str(maxLikeDislikeRatio) + " like for every dislike.")
else:
    print(
        "The video with the best like/dislike ratio is \"" + maxLikeDislikeRatioTitle + "\". It has approximately " + str(maxLikeDislikeRatio) + " likes for every dislike.")
print("")
print("The video with the most comments is \"" + maxCommentsTitle + "\" with " + str(maxComments) + " comments.")
print("")
if maxVideoValue == 0:
    print ("There is no single most popular video from these search criteria.")
else:
    print ("The most popular video from these search criteria is \"" + maxVideoValueTitle + "\".")