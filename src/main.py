import data.make_dataset as load_data_script
import features.build_features as features_script
#import models.train_model as train_model_script
#import models.predict_model as predict_script
import argparse

def main():
    parser = argparse.ArgumentParser(description="Projet IA - Point d'entrée principal.")
    parser.add_argument("action", choices=["laod_data", "transform", "train", "predict", "all"], 
                        help="Action à exécuter : train, train,predict,all.")
    
    args = parser.parse_args()
    
    if args.action == "laod_data":
        print("Appel du script de laod_data...")
        load_data_script.main()
    elif args.action == "transform":
        print("Appel du script transform...")
        features_script.main()
    elif args.action == "train":
        print("Appel du script de train...")
        #train_model_script.main()
    elif args.action == "predict":
        print("Appel du script de prédiction...")
        #predict_script.main()
    elif args.action == "all":
        print("Appel du script de laod_data...")
        load_data_script.main()
        print("Appel du script transform...")
        features_script.main()
        #train_model_script.main()
        #predict_script.main()
    else:
        print("Action non reconnue. Utilisez --help pour voir les options.")

if __name__ == "__main__":
    main()