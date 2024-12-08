GESTURE_BIG_SMILE = {
  "name":"BigSmile",
  "frames":[
    {
      "time":[0.32,0.64],
      "persist": True,
      "params":{
        "BROW_UP_LEFT":1,
        "BROW_UP_RIGHT":1,
        "SMILE_OPEN":0.4,
        "SMILE_CLOSED":0.7
        }
    }],
  "class":"furhatos.gestures.Gesture"
}

GESTURE_RESET_NEUTRAL = {
    "name":"ResetNeutral",
    "frames":[
        {
        "time":[0.32],
        "persist": True,
        "params":{
          "BROW_UP_LEFT":0,
          "BROW_UP_RIGHT":0,
          "SMILE_OPEN":0,
          "SMILE_CLOSED":0
          }
        }],
    "class":"furhatos.gestures.Gesture"
    }