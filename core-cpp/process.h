#include <string>
#include <optional>
#include <iostream>

struct Process{
    std::string pid;
    int burst_time;
    int arrival_time;


    std::optional<int> remaining_time;
    std::optional<int> completion_time;
    std::optional<int> start_time;
    std::optional<float> turnaround_time;
    std::optional<float> waiting_time;

    Process(const std::string& p_id, int b_time, int a_time = 0):
        pid(p_id), burst_time(b_time), arrival_time(a_time){
            remaining_time = burst_time;
        }
};