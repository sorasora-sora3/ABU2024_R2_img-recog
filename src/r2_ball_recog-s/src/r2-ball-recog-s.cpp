#include <stdio.h>
#include <ros/ros.h>
#include <std_msgs/Int16MultiArray.h>

class RecogPublisher
{
private:
    ros::NodeHandle nh_;

    ros::Publisher recog2mod_pub_;
    // ros::Subscriber ball_sub_;
    ros::Subscriber sairo_sub_;

    ros::Timer timer_;

    // std_msgs::Int16 ball_msgs_;
    std_msgs::Int16MultiArray sairo_msgs_;

public:
    RecogPublisher() : nh_()
    {
        recog2mod_pub_ = nh_.advertise<std_msgs::Int16MultiArray>("sairo-detect", 1);
        // ball_sub_ = nh_.subscribe("ball", 10, &RecogPublisher::ballCallback, this);
        sairo_sub_ = nh_.subscribe("sairo-s", 10, &RecogPublisher::sairoCallback, this);
        timer_ = nh_.createTimer(ros::Duration(0.1), &RecogPublisher::timerCallback, this);
    }

    // void ballCallback(const std_msgs::Int16 &msg) // メッセージが来た瞬間に呼ばれる
    // {
    //     ball_msgs_ = msg;
    // }

    void sairoCallback(const std_msgs::Int16MultiArray &msg) // メッセージが来た瞬間に呼ばれる
    {
        sairo_msgs_ = msg;
    }

    void timerCallback(const ros::TimerEvent &e) // 指定した周期(0.1s)毎に呼ばれる
    {
        // recog2mod_pub_.publish(ball_msgs_);
        recog2mod_pub_.publish(sairo_msgs_);
    }
};

int main(int argc, char **argv)
{
    ros::init(argc, argv, "r2-ball-recog-s");

    RecogPublisher RecogPublisher;

    ros::Rate rate(100); // 指定した周期(0.1s)の周波数(10Hz)よりも大きく

    while (ros::ok())
    {
        ros::spinOnce();
        rate.sleep();
    }
    return 0;
}