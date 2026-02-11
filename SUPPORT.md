# Getting help

Be advised, that although the content in this repository is maintained and
curated by Checkmk, it is fully Open Source and there is no commercial support whatsoever!
This is just a side project and we can only work on this on a **part time and best effort basis**.

Of course you can reach out in the [Checkmk Forum (using the 'ansible' tag)](https://forum.checkmk.com/tag/ansible)
or create [issues here](https://github.com/Checkmk/ansible-collection-checkmk.general/issues?q=is%3Aissue+is%3Aopen+sort%3Aupdated-desc).

# Compatibility matrix

The following is a compatibility overview between this collection, Ansible and Checkmk.
We always try to track the most recent Ansible and Checkmk versions.
This table will give you an overview against which Ansible and Checkmk versions we tested a release.
There is of course no guarantees, that there will be no issues at all, but we do our best in testing.
On the other hand this obviously does not limit the collection versions to the Checkmk versions mentioned here.
Most likely the collection will work with most current Checkmk versions.

Collection Version | Checkmk Versions | Ansible Versions | Remarks
--- | --- | --- | ---
0.12.0 | 2.1.0p11, 2.0.0p28 | 2.11, 2.12, 2.13 | None
0.13.0 | 2.1.0p17, 2.0.0p31 | 2.11, 2.12, 2.13 | None
0.14.0 | 2.1.0p17, 2.0.0p31 | 2.11, 2.12, 2.13 | None
0.15.0 | 2.1.0p18, 2.0.0p32 | 2.11, 2.12, 2.13 | None
0.16.0 | 2.1.0p19, 2.0.0p32 | 2.11, 2.12, 2.13 | None
0.16.1 | 2.1.0p19, 2.0.0p32 | 2.11, 2.12, 2.13 | None
0.16.2 | 2.1.0p20, 2.0.0p33 | 2.11, 2.12, 2.13 | None
0.17.0 | 2.1.0p20, 2.0.0p33 | 2.11, 2.12, 2.13 | None
0.17.1 | 2.1.0p21, 2.0.0p33 | 2.11, 2.12, 2.13 | None
0.18.0 | 2.1.0p24, 2.0.0p34 | 2.11, 2.12, 2.13 | None
0.19.0 | 2.1.0p25, 2.0.0p34, 2.2.0b1 | 2.12, 2.13, 2.14 | None
0.20.0 | 2.1.0p25, 2.0.0p34, 2.2.0b2 | 2.12, 2.13, 2.14 | None
0.21.0 | 2.1.0p27, 2.0.0p35, 2.2.0b6 | 2.12, 2.13, 2.14 | None
0.22.0 | 2.1.0p27, 2.0.0p35, 2.2.0b6 | 2.12, 2.13, 2.14 | None
0.23.0 | 2.1.0p28, 2.0.0p36, 2.2.0b8 | 2.13, 2.14, 2.15 | None
1.0.0 | 2.1.0p28, 2.0.0p36, 2.2.0b8 | 2.13, 2.14, 2.15 | Last release of `tribe29.checkmk` before renaming.
2.0.0 | 2.0.0p36, 2.1.0p28, 2.2.0p1 | 2.13, 2.14, 2.15 | First release of `checkmk.general` after renaming.
2.1.0 | 2.0.0p36, 2.1.0p29, 2.2.0p3 | 2.13, 2.14, 2.15 | None
2.2.0 | 2.0.0p36, 2.1.0p29, 2.2.0p3 | 2.13, 2.14, 2.15 | None
2.3.0 | 2.0.0p36, 2.1.0p29, 2.2.0p3 | 2.13, 2.14, 2.15 | None
2.4.0 | 2.0.0p37, 2.1.0p31, 2.2.0p7 | 2.13, 2.14, 2.15 | None
2.4.1 | 2.0.0p37, 2.1.0p31, 2.2.0p7 | 2.13, 2.14, 2.15 | None
3.0.0 | 2.0.0p38, 2.1.0p32, 2.2.0p7 | 2.13, 2.14, 2.15 | Breaking changes to the following modules: `folder`, `host`, `host_group`, `rule`.
3.1.0 | 2.0.0p38, 2.1.0p32, 2.2.0p7 | 2.13, 2.14, 2.15 | None
3.2.0 | 2.0.0p38, 2.1.0p32, 2.2.0p8 | 2.13, 2.14, 2.15 | None
3.3.0 | 2.0.0p39, 2.1.0p35, 2.2.0p12 | 2.13, 2.14, 2.15 | None
3.4.0 | 2.0.0p39, 2.1.0p36, 2.2.0p14 | 2.13, 2.14, 2.15 | None
4.0.0 | 2.0.0p39, 2.1.0p36, 2.2.0p16 | 2.14, 2.15, 2.16 | Breaking changes to the following roles: `agent`, `server`.
4.0.1 | 2.0.0p39, 2.1.0p36, 2.2.0p16 | 2.14, 2.15, 2.16 | None
4.1.0 | 2.0.0p39, 2.1.0p37, 2.2.0p17 | 2.14, 2.15, 2.16 | None
4.2.0 | 2.0.0p39, 2.1.0p38, 2.2.0p19 | 2.14, 2.15, 2.16 | None
4.3.0 | 2.0.0p39, 2.1.0p39, 2.2.0p22 | 2.14, 2.15, 2.16 | None
4.3.1 | 2.0.0p39, 2.1.0p39, 2.2.0p22 | 2.14, 2.15, 2.16 | None
4.4.0 | 2.0.0p39, 2.1.0p41, 2.2.0p24 | 2.14, 2.15, 2.16 | None
4.4.1 | 2.0.0p39, 2.1.0p41, 2.2.0p24 | 2.14, 2.15, 2.16 | None
5.0.0 | 2.1.0p44, 2.2.0p27, 2.3.0p5 | 2.15, 2.16, 2.17 | Breaking changes to the following modules: `lookup_folder`, `rule` and role: `agent`.
5.1.0 | 2.1.0p44, 2.2.0p27, 2.3.0p6 | 2.15, 2.16, 2.17 | None
5.2.0 | 2.1.0p46, 2.2.0p31, 2.3.0p11 | 2.15, 2.16, 2.17 | None
5.2.1 | 2.1.0p46, 2.2.0p32, 2.3.0p12 | 2.15, 2.16, 2.17 | None
5.3.0 | 2.1.0p48, 2.2.0p35, 2.3.0p18 | 2.15, 2.16, 2.17 | None
5.3.1 | 2.1.0p48, 2.2.0p35, 2.3.0p19 | 2.15, 2.16, 2.17 | None
5.3.2 | 2.1.0p49, 2.2.0p37, 2.3.0p23 | 2.15, 2.16, 2.17 | None
5.4.0 | 2.1.0p49, 2.2.0p37, 2.3.0p24 | 2.15, 2.16, 2.17 | None
5.5.0 | 2.1.0p49, 2.2.0p39, 2.3.0p26 | 2.15, 2.16, 2.17 | None
5.6.0 | 2.1.0p49, 2.2.0p40, 2.3.0p27 | 2.15, 2.16, 2.17 | None
5.7.0 | 2.1.0p49, 2.2.0p40, 2.3.0p29 | 2.15, 2.16, 2.17 | None
5.8.0 | 2.2.0p41, 2.3.0p30, 2.4.0b3 | 2.15, 2.16, 2.17 | None
5.9.0 | 2.2.0p41, 2.3.0p31, 2.4.0 | 2.15, 2.16, 2.17 | None
5.10.0 | 2.2.0p42, 2.3.0p33, 2.4.0p2 | 2.15, 2.16, 2.17 | None
5.10.1 | 2.2.0p43, 2.3.0p34, 2.4.0p4 | 2.15, 2.16, 2.17 | None
5.11.0 | 2.2.0p43, 2.3.0p34, 2.4.0p5 | 2.16, 2.17, 2.18 | None
6.0.0 | 2.2.0p44, 2.3.0p34, 2.4.0p7 | 2.16, 2.17, 2.18 | None
6.0.1 | 2.2.0p44, 2.3.0p34, 2.4.0p8 | 2.16, 2.17, 2.18 | None
6.1.0 | 2.2.0p44, 2.3.0p35, 2.4.0p9 | 2.16, 2.17, 2.18 | None
6.2.0 | 2.2.0p45, 2.3.0p35, 2.4.0p9 | 2.16, 2.17, 2.18 | None
6.2.1 | 2.2.0p45, 2.3.0p35, 2.4.0p9 | 2.16, 2.17, 2.18 | None
6.2.2 | 2.2.0p45, 2.3.0p36, 2.4.0p10 | 2.16, 2.17, 2.18 | None
6.2.3 | 2.2.0p46, 2.3.0p38, 2.4.0p13 | 2.17, 2.18, 2.19 | None
6.3.0 | 2.2.0p47, 2.3.0p40, 2.4.0p15 | 2.17, 2.18, 2.19 | None
6.3.1 | 2.2.0p47, 2.3.0p40, 2.4.0p15 | 2.17, 2.18, 2.19 | None
6.4.0 | 2.2.0p47, 2.3.0p40, 2.4.0p16 | 2.17, 2.18, 2.19 | None
6.4.1 | 2.2.0p47, 2.3.0p41, 2.4.0p16 | 2.17, 2.18, 2.19 | None
6.5.0 | 2.2.0p47, 2.3.0p41, 2.4.0p17 | 2.18, 2.19, 2.20 | None
6.6.0 | 2.2.0p47, 2.3.0p41, 2.4.0p18 | 2.18, 2.19, 2.20 | None
6.6.1 | 2.2.0p47, 2.3.0p41, 2.4.0p18 | 2.18, 2.19, 2.20 | None
6.7.0 | 2.2.0p47, 2.3.0p41, 2.4.0p19 | 2.18, 2.19, 2.20 | None
7.0.0 | 2.2.0p47, 2.3.0p42, 2.4.0p19 | 2.18, 2.19, 2.20 | None
7.0.1 | 2.2.0p47, 2.3.0p42, 2.4.0p20 | 2.18, 2.19, 2.20 | None
7.1.0 | 2.2.0p47, 2.3.0p42, 2.4.0p21 | 2.18, 2.19, 2.20 | None
