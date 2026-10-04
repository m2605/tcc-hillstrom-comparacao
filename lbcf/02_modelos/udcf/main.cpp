#include <cstdlib>
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

// Hillstrom: argumentos de linha de comando (sem argumentos = configuracao dos autores)
//   ./UDCF <imbalance_penalty> <stabilize_splits 0|1> <treino> <teste> <saida>
int main(int argc, char* argv[])
{
    double imbalance_penalty = 0.01;   // valor de default_options(true,1) dos autores
    bool stabilize_splits = true;      // valor do udcf_trainer dos autores
    std::string treino = "train_data_UDCF.csv";
    std::string teste = "test_data_UDCF.csv";
    std::string saida = "UDCF_uplift";
    if (argc > 1) imbalance_penalty = std::atof(argv[1]);
    if (argc > 2) stabilize_splits = (std::atoi(argv[2]) != 0);
    if (argc > 3) treino = argv[3];
    if (argc > 4) teste = argv[4];
    if (argc > 5) saida = argv[5];
    std::cout << "imbalance_penalty=" << imbalance_penalty
              << " stabilize_splits=" << stabilize_splits << std::endl;
    
    char tmp[256];
    getcwd(tmp, 256);
    std::cout << "Current working directory: " << tmp << std::endl;
    // /UDCF/core/build  
    auto data_vec = load_data(treino);
    Data data(data_vec);
    data.set_outcome_index(11);
    data.set_treatment_index({12,13});
//     data.set_outcome_index(4);
//     data.set_treatment_index({5,6,7});
    
    
    auto data_vec2 = load_data(teste);
    Data data2(data_vec2);
//     data2.set_outcome_index(4);
//     data2.set_treatment_index({5});
    data2.set_outcome_index(11);
    data2.set_treatment_index({12});
    size_t num_treatments = 2;   
    
    ForestTrainer trainer = udcf_trainer(num_treatments, 1, stabilize_splits);   
    // mesmos valores de ForestTestUtilities::default_options(true,1), exceto imbalance_penalty
    ForestOptions options(300, 1, 0.5, 3, 50, true, 0.5, true, 0.05,
                          imbalance_penalty, 40, 42, std::vector<size_t>(), 0);
    Forest forest = trainer.train(data, options);
    ForestPredictor predictor = udcf_predictor(1, num_treatments, 1);  
    std::vector<Prediction> predictions = predictor.predict(forest, data, data2, false);
    update_predictions_file(saida, predictions);
    /*
    for( int i = 1; i <= 7;i = i + 1 ){
        std::string path="../test/forest/resources/MBCF/MBCF_train"+std::to_string(i)+".csv";
        std::cout<<path<<std::endl;
        auto data_vec = load_data(path);
        auto data_vec2 = load_data("../test/forest/resources/MBCF/test_data.csv");
        Data data(data_vec);
        data.set_outcome_index(28);
        data.set_treatment_index(29);
        data.set_instrument_index(29);

        double reduced_form_weight = 0.0;
        bool stabilize_splits = false;

        ForestTrainer trainer = instrumental_trainer(reduced_form_weight, stabilize_splits);
        ForestOptions options = ForestTestUtilities::default_options(true,1);

        Forest forest = trainer.train(data, options);
        Data data2(data_vec2);
        data2.set_outcome_index(28);
        data2.set_treatment_index(29);
        data2.set_instrument_index(29);
        ForestPredictor predictor = instrumental_predictor(4);
        std::vector<Prediction> predictions2 = predictor.predict(forest, data2, data2, false);
        std::string path_predict="../test/forest/resources/MBCF/MBCF_uplift"+std::to_string(i)+".csv";
        update_predictions_file(path_predict, predictions2);
    }
    */
    
    
      
    return 0;
}
