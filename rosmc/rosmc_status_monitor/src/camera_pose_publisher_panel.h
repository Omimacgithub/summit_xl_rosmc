//
// The BSD 3-Clause License
//
// Copyright (c) 2022, DLR-RM All rights reserved.
//
// Redistribution and use in source and binary forms, with or without 
// modification, are permitted provided that the following conditions are met:
//
// 1. Redistributions of source code must retain the above copyright notice, 
//    this list of conditions and the following disclaimer.
//
// 2. Redistributions in binary form must reproduce the above copyright notice, 
//    this list of conditions and the following disclaimer in the documentation 
//    and/or other materials provided with the distribution.
//
// 3. Neither the name of the copyright holder nor the names of its contributors 
//    may be used to endorse or promote products derived from this software 
//    without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
// AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
// IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
// DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
// FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
// DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
// SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
// CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
// OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
// 
// Contributors:
// Ryo Sakagami <ryo.sakagami@dlr.de>
//
#ifndef ROSMC_STATUS_MONITOR_CAMERA_POSE_PUBLISHER_PANEL_H
#define ROSMC_STATUS_MONITOR_CAMERA_POSE_PUBLISHER_PANEL_H

#ifndef Q_MOC_RUN
#include <ros/ros.h>
#include <rviz/panel.h>
#endif

namespace rosmc_status_monitor
{

class CameraPosePublisherPanel : public rviz::Panel
{
Q_OBJECT

public:
  CameraPosePublisherPanel( QWidget *parent = 0 );

  ~CameraPosePublisherPanel();

  virtual void load( const rviz::Config &config );

  virtual void save( rviz::Config config ) const;

protected:
  void timerCallback( const ros::TimerEvent &event );
  ros::Publisher pose_stamped_publisher_;
  ros::NodeHandle nh_;
  ros::Timer timer_;
};

}  // end namespace rosmc_status_monitor

#endif //ROSMC_STATUS_MONITOR_CAMERA_POSE_PUBLISHER_PANEL_H
