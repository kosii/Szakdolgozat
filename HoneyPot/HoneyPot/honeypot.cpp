#include "honeypot.h"

honeypot::honeypot(QObject *parent)
	: QObject(parent)
{
	QObject::connect(this, SIGNAL(Signal(int)), this, SLOT(Slot1(int)));
}

honeypot::~honeypot()
{

}

int honeypot::Slot1(int v){

	return 1;
}

Q_DECLARE_OPERATORS_FOR_FLAGS(honeypot::Options);