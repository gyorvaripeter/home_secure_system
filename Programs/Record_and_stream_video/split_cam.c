
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <fcntl.h>
#include <unistd.h>
#include <stropts.h>
#include <signal.h>

#define MAX_FILENAME_SIZE 100

//fajlleiro kimenet az eppen megnyitott adatfajlhoz
static int fd_out;

void sig_handler(int signum) {

  if (fd_out >= 0) {    
    // az osszes irasi sor uritese
    ioctl(fd_out, I_FLUSH, FLUSHW);

    // adat fajl zarasa
    close(fd_out);
  }

  exit(0);
}

int main(void) {
  char in_array[1024];
  int nBytes;
  char filename[MAX_FILENAME_SIZE];
  struct timeval ts;  

  // Register signal handler
  signal(SIGINT, sig_handler);

  // fd_out inicializalasa
  fd_out = -1;

  // jelenlegi idopont az egyedi fajlnevekhez
  gettimeofday(&ts, NULL);

  // fajlnev generalas
  snprintf(filename, MAX_FILENAME_SIZE, "raspiVid-%u-%u.h264", ts.tv_sec, ts.tv_usec);

  // megnyitja a fajlt adatirasra
  fd_out = open(filename, O_CREAT | O_WRONLY, S_IRUSR | S_IWUSR | S_IRGRP | S_IWGRP);

  // adatok olvasasa az stdinbol
  nBytes = read(STDIN_FILENO, in_array, sizeof(in_array));

  // adatot olvas az stdinbol az iteracioba
  // amig adatot ir a fileba, es
  // az stdoutba is
  while(nBytes > 0) {
    //adatiras a fajlba
    write(fd_out, (const void*)in_array, nBytes);

    // az stdoutra is irjon adatot
    write(STDOUT_FILENO, (const void*)in_array, nBytes);

    // az osszes irasi sor kiuritese
    ioctl(fd_out, I_FLUSH, FLUSHW);

    // a kovetkezo elerheto adatdarab az stdinbol
    nBytes = read(STDIN_FILENO, in_array, sizeof(in_array)); 
  }

  // adatfajl lezarasa
  close(fd_out);
  fd_out = -1;

  return 0;
}
