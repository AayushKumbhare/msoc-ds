import dotenv
import os
import requests
import json

dotenv.load_dotenv()
MSOC_API_KEY = os.getenv("MSOC_API_KEY")

"""API response for all activities for MSOC"""
activity_url = "https://connect-us.catapultsports.com/api/v6/activities/"
headers = {
    "accept": "application/json",
    "authorization": f"Bearer {MSOC_API_KEY}"
}
activity_response = requests.get(activity_url, headers=headers)

"""API response for all athletes for MSOC"""
athlete_url = "https://connect-us.catapultsports.com/api/v6/athletes/"
athlete_response = requests.get(athlete_url, headers=headers)

def get_activities():
    activities = []
    try:
        for activity in activity_response.json():
            activities.append(activity['id'])
        return activities
    except Exception as e:
        print(f"Error getting activities: {e}")
        return []

def get_athlete_id():
    athletes = []
    try:
        for athlete in athlete_response.json():
            athletes.append(athlete['id'])
        return athletes
    except Exception as e:
        print(f"Error getting athletes: {e}")
        return []

def get_response(activities_id, athletes_id):
    # Create data folder if it doesn't exist
    data_folder = "athlete-activity-data"
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    
    for activity_id, athlete_id in zip(activities_id, athletes_id):
        """API response for data on an athlete's activity"""
        sensor_url = f"https://connect-us.catapultsports.com/api/v6/activities/{activity_id}/athletes/{athlete_id}/sensor"
        
        try:
            response = requests.get(sensor_url, headers=headers)
            
            if response.status_code == 200:
                filename = f"activity_{activity_id}_athlete_{athlete_id}.json"
                file_path = os.path.join(data_folder, filename)

                # Save the data
                with open(file_path, "w") as f:
                    json.dump(response.json(), f, indent=4)
                print(f"Data for athlete {athlete_id} in activity {activity_id} saved to {file_path}")
            else:
                print(f"Athlete {athlete_id} not found in activity {activity_id}. Status code: {response.status_code}")
                
        except Exception as e:
            print(f"Error processing athlete {athlete_id} in activity {activity_id}: {e}")
            continue

if __name__ == "__main__":
    activities = get_activities()
    athletes = get_athlete_id()
    if activities and athletes:
        get_response(activities, athletes)
    else:
        print("No activities or athletes found.")\
    
