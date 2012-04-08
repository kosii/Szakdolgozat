#ifndef NO_SIGNALS_H
#define NO_SIGNALS_H

#include <QObject>

class no_signals : public QObject
{
	Q_OBJECT

public:
	no_signals(QObject *parent);
	~no_signals();

private:
	
};

#endif // NO_SIGNALS_H
