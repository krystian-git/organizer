a = {'nic':{'_init':True}}
b = 'nic'
c = 'po'

a[b][c] = True
a[b]['czop'] = True
a[b]['czo'] = True
a[b]['czp'] = True
a[b]['cop'] = True
for key, value in a.items():
    print(len(value.keys()))
print(a)