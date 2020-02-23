#include "network.h"

#include <iostream>

using namespace std;

double func1(double x, double y)
{
    int x_ = x;
    int y_ = y;
    cout << x_ << " " << y_ << endl;

    return x_ ^ y_;
}

double func2(double x, double y)
{
    return x*x+y*y;
}

double func3(double x, double y)
{
    return 0;
}

int main()
{
    /*vector<Weights> w {
        {{0.5, 0.5},
         {0.5, 0.5}},

        {{1}, {1}}
    };*/
    vector<Weights> w {
        {
            {0.5, 0.5, 0.5},
            {0.5, 0.5, 0.5}
        },

        {
            {0.5, 0.5, 0.5},
            {0.5, 0.5, 0.5},
            {0.5, 0.5, 0.5}
        },

        {
            {1}, {1}, {1}
        }
    };
    Network n(w);

    /*cout << 0 << " " << n.activate_(0) << endl;
    cout << 0.5 << " " << n.activate_(0.5) << endl;
    cout << 1 << " " << n.activate_(1) << endl;
    cout << 2 << " " << n.activate_(2) << endl;*/

    vector<vector<double>> features;
    vector<double> targets;

    int N = 1000;
    for (int i = 0; i < N; ++i) {
        vector<double> p;
        p.push_back(rand01());
        p.push_back(rand01());
        features.push_back(p);

        targets.push_back(func2(p[0], p[1]));
    }
    //features.push_back({1, 1});
    //targets.push_back(0);

    n.train(features, targets);

    n.print();

    for (int i = 0; i < 10; ++i) {
        vector<double> p;
        p.push_back(rand01());
        p.push_back(rand01());

        double res = n.run(p);

        cout << p[0] << ", " << p[1] << " : " << res << endl;
    }
    //double res = n.run({-5, 5});
    //cout << "Sum: " << res << endl;
    return 0;
}
