#include <stdio.h>
#include <unordered_map>
#include <string>
#include <adns.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <unistd.h>

#include "namelookup.h"
#include "domainNameLoader.h"

using namespace std;

void adnsloopup(unordered_set<string> &domainSet);
void query_callback(void *arg, adns_answer *answer, int count);

int main(int argc, char *argv[])
{
    // 1. read domain list
    AlexaDomainNameLoader alexaDomainNameLoader("./data/alexa-top-10.csv");
    alexaDomainNameLoader.load();

    // 3. aggregate domain name
    unordered_set<string> domainNameSet = alexaDomainNameLoader.getDomainNameSet();

    // 2. lookup domain name
    adnsloopup(domainNameSet);

    return 0;
}

void adnsloopup(unordered_set<string> &domainSet)
{
    adns_state ads;
    adns_initflags initflags = (adns_initflags)(adns_if_nosigpipe | adns_if_noerrprint);
    adns_init(&ads, initflags, NULL);

    for (auto domain : domainSet)
    {
        adns_query query;
        adns_queryflags flags = adns_qf_owner;
        adns_submit(ads, domain.c_str(), adns_r_a, flags, query_callback, &query);
    }

    adns_finish(ads);
}

void query_callback(void *arg, adns_answer *answer, int count)
{
    const char *domain = (char *)arg;

    if (count > 0)
    {
        printf("DNS Query Result for %s:\n", domain);
        for (int i=0; i<count; i++)
        {
            if (answer[i].status == adns_s_ok)
            {
                if (answer[i].status == adns_s_ok)
                {
                    if (answer[i].type == adns_r_a)
                    {
                        printf("IPv4 Address: %s\n", inet_ntoa(answer[i].rrs.addr->addr.inet.sin_addr));
                    }else if (answer[i].type == adns_r_aaaa)
                    {
                        char addr_str[INET6_ADDRSTRLEN];
                        inet_ntop(AF_INET6, &answer[i].rrs.addr->addr.inet6.sin6_addr, addr_str, INET6_ADDRSTRLEN);
                        printf("IPv6 Address: %s\n", addr_str);
                    }
                }else
                {
                    printf("DNS Query Failed: %s\n", adns_strerror(answer[i].status));
                }
                
            }else
            {
                printf("No DNS record found for %s\n", domain);
            }
        }
    }
}