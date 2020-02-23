#include <vector>
#include <cmath>
#include <cstdlib>

// fixme
#include <iostream>

using std::vector;

//fixme
using namespace std;

typedef vector<vector<double>> Values;
typedef vector<vector<double>> Weights;
typedef vector<double> Input;

double rand01()
{
    return abs((double) rand() / RAND_MAX);
}

class Network {
public:
    Network(const vector<int>& layers)
    : height_(layers.size()), layers_(layers)
    {
    
    
    }

    Network(const vector<Weights>& weights)
    : height_(weights.size() + 1), weights_(weights)
    {
        layers_.push_back(weights[0].size());
        for (int i = 0; i + 1 < height_; ++i) {
            layers_.push_back(weights[i][0].size());
        }
    }

    void print()
    {
        /*
        cout << "Layers: ";
        for (int i = 0; i < height_; ++i) {
            cout << layers_[i] << " ";
        }
        cout << endl;
        */

        cout << "Weights: " << endl;
        for (int i = 0; i < weights_.size(); ++i) {
            for (int from = 0; from < weights_[i].size(); ++from) {
                for (int to = 0; to < weights_[i][0].size(); ++to) {
                    cout << weights_[i][from][to] << " ";
                }
                cout << endl;
            }
            cout << endl;
        }

        /*cout << "Values:" << endl;
        for (int i = 0; i < height_; ++i) {
            for (int j = 0; j < layers_[i]; ++j) {
                cout << values_[i][j] << " ";
            }
            cout << endl;
        }*/
    }

    void init_weights()
    {
        // fixme: will fail
        for (int layer = 0; layer + 1 < height_; ++layer) {
            for (int from = 0; from < layers_[layer]; ++from) {
                for (int to = 0; to < layers_[layer + 1]; ++to) {
                    weights_[layer][from][to] = abs((double) rand() / RAND_MAX);
                }
            }
        }
    }

    void train(const vector<Input>& features, const vector<double>& targets)
    {
        if (features.size() != targets.size()) {
            throw std::runtime_error("Bad training data");
        }

        //init_weights();
        print();
        for (int i = 0; i < targets.size(); ++i) {
            double result = run(features[i]);
            run_back_propagation(targets[i]);
            print();
        }
    }

    // values_ -- это значения на нейронах
    // weights_ -- это набор табличек веса i - i+1
    double run(const Input& input)
    {
        values_.clear();
        values_.push_back(input);

        double arg;
        for (int step = 0; step + 1 < height_; ++step) {
            values_.push_back(vector<double>());
            for (int to = 0; to < layers_[step + 1]; ++to) {
                arg = 0;
                for (int from = 0; from < layers_[step]; ++from) {
                    arg += weights_[step][from][to] * values_[step][from];
                }
                if (step + 2 < height_)
                    arg = activate_(arg);
                values_[step + 1].push_back(arg);
            }
        }

        return arg;
    }

    void run_back_propagation(double etalon)
    {
        vector<Weights> old_weights = weights_;

        Values deltas(height_);

        for (int step = height_ - 1; step > 0; --step) {
            for (int to = 0; to < layers_[step]; ++to) {
                double o_j = values_[step][to];

                double delta_j;
                if (step == height_ - 1) {
                    delta_j = -activate_(o_j) * (1 - activate_(o_j)) * (etalon - o_j);
                }
                else {
                    double sum = 0;
                    for (int child = 0; child < layers_[step + 1]; ++child) {
                        sum += old_weights[step][to][child] * deltas[step + 1][child];
                    }
                    delta_j = activate_(o_j) * (1 - activate_(o_j)) * sum;
                }
                deltas[step].push_back(delta_j);

                for (int from = 0; from < layers_[step - 1]; ++from) {
                    //cout << "Before " << from << " "  << to << endl;
                    weights_[step - 1][from][to] += (-1) * delta_j * values_[step - 1][from];
                }
            }
        }
    }

//private:
    double activate_(double x)
    {
        return 1.0 / (1 + exp(-x));
    }

    vector<Weights> weights_;
    Values values_;
    vector<int> layers_;

    int height_;
};
