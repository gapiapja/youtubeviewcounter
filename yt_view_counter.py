import os
import google_auth_oauthlib.flow #pip install google-auth-oauthlib
import googleapiclient.discovery #pip install google-api-python-client
import googleapiclient.errors
import pprint
from time import sleep

#initialize permissions
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

#to displau data
pp = pprint.PrettyPrinter(indent=2)
def main():
    #setup
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    api_service_name = "youtube"
    api_version = "v3"

    client_secrets_file = "client_secret.json"

    youtube = [];
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube.append(googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials))

    count = 0;
    curr_api = 0;
    
    while(True): 

        # Request (This is what asks Youtube API for the video data)
        try:
            request = youtube[curr_api].videos().list(
                part="snippet,statistics",
                id="uSBSd9WK90M"
            )
            response = request.execute()

            data = response["items"][0];
            vid_snippet = data["snippet"];

            title = vid_snippet["title"];

            views = str(data["statistics"]["viewCount"]);
            
            print("");
            print("Title of Video: " + title);
            print("Number of Views: " + views);

            change = (views not in title);

            if(change):
                title_upd = "Video ini punya " + format(int(views), ",d") + " Penonton, Explained";
                vid_snippet["title"] = title_upd;

                request = youtube[curr_api].videos().update(
                    part="snippet",
                    body={
                        "id": "uSBSd9WK90M",
                        "snippet": vid_snippet
                    }
                )
                response = request.execute()
                
                print("Worked!" + str(count));
                sleep(475);
            count += 1;
            
            
        except:
            print("Error, trying again");

        count += 1;
        sleep(44);
        
        
#run program
if __name__ == "__main__":
    main()
