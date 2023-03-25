# Plaintext pleasure (very easy)
For this challenge we could open the capture file using wireshark.
However I think a more classical approach is better here:

```shell
➜  forensics strings capture.pcap | grep HTB
HTB{th3s3_4l13ns_st1ll_us3_HTTP}
```
