#! /usr/local/bin/python3

import sys
import argparse
import datetime

class TrackTimes:
    def __init__(self, tracktimes_file, tracktitles_file, tracklist_file):
        """Return a new Truck object."""
        self.tracktimes_file = tracktimes_file
        self.tracktitles_file = tracktitles_file
        self.tracklist_file = tracklist_file
        self.new_tracklist = None
        self.tracktimes=[]
        self.tracktimes_in_milliseconds=[]
        self.tracknames=[]
        self.starttimes=[]
 
    def get_time(self,ms):
        s=ms/1000
        m,s=divmod(s,60)
        h,m=divmod(m,60)
        d,h=divmod(h,24)
        s=round(s,8)
        return d,h,m,s

    def sum_time(self,h,m,s,ms):
        time_in_milliseconds=( h*60*1000) + (m*60*1000) + (s*1000) + (ms)
        return (time_in_milliseconds)

    def sum_list_partial(self,my_list,start_index,end_index):
        total = 0
        for i in range(start_index, end_index+1):
            if (i <= len(my_list)-1):
                total+=my_list[i]
        return total

    def generate_tracklist(self):
        with open(self.tracktimes_file) as file:
            self.tracktimes = file.readlines()
        with open(self.tracktitles_file) as file:
            self.tracknames = file.readlines()
        for i in range(len(self.tracktimes)):
            self.tracktimes[i] = self.tracktimes[i].rstrip().split(':')
            self.tracktimes[i][len(self.tracktimes[i])-1] = [int(s) for s in self.tracktimes[i][ len(self.tracktimes[i])-1 ].split('.')]
            self.tracktimes[i][0] =  int(self.tracktimes[i][0] )        # hours
            self.tracktimes[i][1] =  int(self.tracktimes[i][1] )        # minutes
            self.tracktimes[i][2][0]  =  int(self.tracktimes[i][2][0] ) # seconds
            self.tracktimes[i][2][1] = int(self.tracktimes[i][2][1] )   # milliseconds
            total_track_length=self.sum_time(self.tracktimes[i][0],self.tracktimes[i][1],self.tracktimes[i][2][0],self.tracktimes[i][2][1])
            self.tracktimes_in_milliseconds.append(total_track_length)
                
        for i in range(len(self.tracktimes_in_milliseconds)):
            start_time = self.sum_list_partial(self.tracktimes_in_milliseconds, 0, i-1 )
            self.starttimes.append(start_time)

        file = open(self.tracklist_file,"w")
        for track_name, start_time in zip(self.tracknames,self.starttimes):
            d,h,m,s=self.get_time(start_time)
            file.write(track_name.rstrip())
            file.write(" - %d:%d:%d \n" % (h,m,s))
        file.close()




            
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('tracktimes', help='input tracktimes file')
    parser.add_argument('tracktitles', help='input trackttiles file')
    parser.add_argument('tracklist', help='output tracklist file')
    args = parser.parse_args()

    myTrackTimes=TrackTimes(args.tracktimes,args.tracktitles,args.tracklist)
    myTrackTimes.generate_tracklist()



if __name__ == '__main__':

    main()
