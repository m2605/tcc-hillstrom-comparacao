#include <iostream>


#include <string>

#include <unistd.h>

#include "tree/Tree.h"

#include "prediction/DefaultPredictionStrategy.h"
#include "commons/utility.h"
#include "forest/ForestPredictor.h"
#include "forest/ForestTrainer.h"
#include "utilities/FileTestUtilities.h"
#include "utilities/ForestTestUtilities.h"

#include "forest/ForestTrainers.h"
#include "forest/ForestPredictors.h"
using namespace grf;

void update_predictions_file(const std::string& file_name,
                             const std::vector<Prediction>& predictions) {
  std::vector<std::vector<double>> values;
  values.reserve(predictions.size());
  for (const auto& prediction : predictions) {
    values.push_back(prediction.get_predictions());
  }
  FileTestUtilities::write_csv_file(file_name, values);
  std::cout << "success! predictions dump to " << file_name << std::endl;
}

// Hillstrom: argumentos de linha de comando
//   ./MBCF <pasta_dados> <pasta_saida>
int main(int argc, char* argv[])
{
    std::string dados = ".";
    std::string saida = ".";
    if (argc > 1) dados = argv[1];
    if (argc > 2) saida = argv[2];
    
    char tmp[256];
    getcwd(tmp, 256);
    std::cout << "Current working directory: " << tmp << std::endl;
    // /UDCF/core/build
    
    /*
    auto data_vec = load_data("../test/forest/resources/UDCF/UDCF_train.csv");
    Data data(data_vec);
    data.set_outcome_index(28);
    data.set_treatment_index({29,30,31,32,33,34,35});
    
    
    auto data_vec2 = load_data("../test/forest/resources/UDCF/test_data.csv");
    Data data2(data_vec2);
    data2.set_outcome_index(28);
    data2.set_treatment_index({29});
    
    size_t num_treatments = 7;   
    
    ForestTrainer trainer = udcf_trainer(num_treatments, 1, true);   
    ForestOptions options = ForestTestUtilities::default_options();
    Forest forest = trainer.train(data, options);
    ForestPredictor predictor = udcf_predictor(1, num_treatments, 1);  
    std::vector<Prediction> predictions = predictor.predict(forest, data, data2, false);
    update_predictions_file("../test/forest/resources/UDCF/UDCF_uplift.csv", predictions);
    */
    for( int i = 1; i <= 2;i = i + 1 ){
        std::string path=dados+"/MBCF_train_"+std::to_string(i)+".csv";
        std::cout<<path<<std::endl;
        auto data_vec = load_data(path);
//         auto data_vec2 = load_data("/home/xueshengjie/.jupyter/CausalML/paper_data_final/WWW2021_binary_test_all_uw20.csv");
        auto data_vec2 = load_data(dados+"/test_data_MBCF.csv");
        Data data(data_vec);
//         data.set_outcome_index(5);
//         data.set_treatment_index(4);
//         data.set_instrument_index(5);
        data.set_outcome_index(11);
        data.set_treatment_index(12);
        data.set_instrument_index(12);

        double reduced_form_weight = 0.0;
        bool stabilize_splits = false;

        ForestTrainer trainer = instrumental_trainer(reduced_form_weight, stabilize_splits);
        ForestOptions options = ForestTestUtilities::default_options(true,1);

        Forest forest = trainer.train(data, options);
        Data data2(data_vec2);
        data2.set_outcome_index(11);
        data2.set_treatment_index(12);
        data2.set_instrument_index(12);
        ForestPredictor predictor = instrumental_predictor(5);
        std::vector<Prediction> predictions2 = predictor.predict(forest, data2, data2, false);
        std::string path_predict=saida+"/MBCF_uplift_"+std::to_string(i)+".csv";
        update_predictions_file(path_predict, predictions2);
    }
    
    
    
      
    return 0;
}
