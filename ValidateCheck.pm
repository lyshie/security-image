#!/usr/bin/perl -w
#
#    Copyright (C) 2008~2014 SHIE, Li-Yi (lyshie) <lyshie@mx.nthu.edu.tw>
#
#    https://github.com/lyshie
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation,  either version 3 of the License,  or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not,  see <http://www.gnu.org/licenses/>.
#
#
#
use strict;
use warnings;
#
BEGIN { $INC{'ValidateCheck.pm'} ||= __FILE__ }

package ValidateCheck;
use LWP::UserAgent;

our @ISA    = qw(Exporter);
our @EXPORT = qw(checkRemoteValidate
);

my $URL = "http://service.oz.nthu.tw/cgi-bin/validate/validate_check.cgi";

sub checkRemoteValidate {
    my $validate = shift || '';
    my $host     = shift || '';

    $validate =~ s/[^\d]//g;
    $host =~ s/[^a-zA-Z0-9\.\-\_]//g;

    my $ua = LWP::UserAgent->new;
    $ua->timeout(10);

    my $response = $ua->get("$URL?validate=$validate&host=$host");

    if ( $response->is_success ) {
        return $response->content;
    }
    else {    # bypass
        return -1;
    }
}
