# Usage:
# find heat -type f -name '*.py' | xargs sed -i '' -f ~/dev/perso/six.sed

# Replace types
s/six\.string_types/str/g
s/six\.text_type/str/g
s/six\.integer_types/int/g
#s/six\.b(\(.*\))/\1/g
#
## Replace imports
#/^import six$/d
s/from six\.moves\.urllib \(.*\)/from urllib \1/g
s/from six\.moves import urllib/import urllib/g

# Replace six moves
s/six\.moves\.xrange/range/g
s/six\.moves\.range/range/g
s/six\.moves\.map/map/g
s/six\.moves\.zip/zip/g

# Replace iterables
s/six\.iteritems(\(.*\))/\1\.items\(\)/g
s/six\.itervalues(\(.*\))/\1\.values\(\)/g
s/six\.iterkeys(\(.*\))/\1\.keys\(\)/g
#
/@six\.python_2_unicode_compatible/d
