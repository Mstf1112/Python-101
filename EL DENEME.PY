import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

## Statik durundaki görseller

IMAGE_FILES = []
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=2,
    min_detection_confidence=0.5) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    ## ********** GÖRÜNTÜ İŞLEME **********

    ## Görüntüden yansıyan ışığı y eksenin de oturtmak için görseli çeviriyoruz 

    image = cv2.flip(cv2.imread(file), 1)
    ## BGE'den RGB ye dönüştürme yapıyoruz bu sayede renk gamında sorun olmuyor

    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    ## Görüntü üzerine el işaretlerini (Hand landmarks ) yazdırma işlemi

    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      continue

    image_height, image_width, _ = image.shape
    annotated_image = image.copy()

    for hand_landmarks in results.multi_hand_landmarks:

      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )

      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())

    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    ## HandLandmarkları el üzerinde göreselleştirme.
    if not results.multi_hand_world_landmarks:
      continue
    for hand_world_landmarks in results.multi_hand_world_landmarks:
      mp_drawing.plot_landmarks(
        hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)

      ## ********** WEBCAM DE YAZDIRMA **********
## Webcam Açılması:
cap = cv2.VideoCapture(0)
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      ## Eğer video yükleniyorsa,Continue yerine Break kullan // Sorun oluşursa diye ek bilgi
      continue

    
    ## performası arrtırmak için görüntüyü yazılamaz hala çevir
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    ## Webcam açıldıktan sonra tanınan elin üzerine handlandmarkları yazdırma
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
           ## el açık ve kapalı iken ekrana yazdırma bu mantık üzerinden karakter üzerindeki atak animasyonları çalışacak clas haline getirildikten sonra
           ## main.py dosyası üzerinden çekilecek
        orta_p_a, orta_p_u = hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y
        orta_p_a1, orta_p_u1 = hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y

        font = cv2.FONT_HERSHEY_PLAIN
        
        if orta_p_u1 > orta_p_u:
                cv2.putText(image, "KAPALI", (10, 50), font, 4, (0, 0, 0), 3)
        else:
                cv2.putText(image, "ACIK", (10, 50), font, 4, (0, 0, 0), 3)
        ## 
        
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    ## Görüntü işlenditen sonra bir kez daha ters çeviriyoruz çünkü hali hazırda ters çevirdiğimiz görüntü
    ## biz görüntüledeğimiz de ekrana düşen görüntü y eksenin de ters olacaktır bunu tersine çevirmek için biz tekrar görüntüyü tersine çeviriyoruz 

    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

