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
use CGI qw(:standard);
use FindBin qw($Bin);

#use POSIX;

my $VALIDATE_PATH = "/tmp/my_validate";
my %_HOSTS        = (
    '64' => 1,
    '63' => 1,
);

my $_DATA = "";
my $_HOST = "";

sub checkHost {
    my $host = shift;
    $host =~ s/[^a-zA-Z0-9\.\-\_]//g;

    return 1 if ( $host eq 'default' );

    return $_HOSTS{$host};
}

sub _getParams {
    my @all = param('validate');

    # lyshie_20080626: allow multiple variables
    foreach (@all) {
        if ( defined($_) && ( $_ ne '' ) ) {
            $_DATA = $_;
        }
    }
    $_DATA = '' unless defined($_DATA);
    $_DATA =~ s/[^\d]//g;

    $_HOST = param('host') || '';
}

sub _checkValidate {
    my $data = shift || '';
    my $host = shift || '';

    $data =~ s/[^\d]//g;

    return 0 unless ( checkHost($host) );
    return 0 unless ( -f "$VALIDATE_PATH/$host/$data" );

    #open(FH, "$VALIDATE_PATH/$host/$data");
    #my $time = <FH> || 0;
    #chomp($time);
    #close(FH);
    my $time = ( stat("$VALIDATE_PATH/$host/$data") )[10] || 0;
    unlink("$VALIDATE_PATH/$host/$data");

    if ( time() - $time < 10 * 60 ) {
        return 1;
    }
    else {
        return 0;
    }
}

sub checkValidate {
    _getParams();
    print header();
    printf( "%d", _checkValidate( $_DATA, $_HOST ) );
}

checkValidate();
